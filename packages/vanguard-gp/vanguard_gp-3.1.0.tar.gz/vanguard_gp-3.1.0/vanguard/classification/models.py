# © Crown Copyright GCHQ
#
# Licensed under the GNU General Public License, version 3 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.gnu.org/licenses/gpl-3.0.en.html
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Contains model classes to enable classification in Vanguard.
"""

import warnings
from typing import Any, Optional, Union

import gpytorch
import torch
from gpytorch import settings
from gpytorch.distributions import MultivariateNormal
from gpytorch.means import ZeroMean
from gpytorch.models import ExactGP
from gpytorch.utils.warnings import GPInputWarning
from linear_operator import LinearOperator
from linear_operator.operators import DiagLinearOperator
from torch import Tensor
from typing_extensions import override

from vanguard.models import ExactGPModel
from vanguard.utils import DummyDistribution


class DummyKernelDistribution(DummyDistribution):
    """
    A dummy distribution to hold a kernel matrix and some one-hot labels.
    """

    # TODO: Lying to the type checker here feels like bad code, and should only be a very temporary measure. Should
    #  probably just inherit from Distribution, and type hint downstream code to expect an arbitrary Distribution.
    # https://github.com/gchq/Vanguard/issues/394
    __class__ = MultivariateNormal

    def __init__(self, labels: Union[Tensor, LinearOperator], kernel: Union[Tensor, LinearOperator]) -> None:
        """
        Initialise self.

        :param labels: The one-hot labels, shape: torch.Size([n_points, num_classes]).
        :param kernel: The kernel matrix.
        """
        self.labels = labels
        self.kernel = kernel

        try:
            self.mean = self.kernel @ self.labels.to_dense()
            self.covariance_matrix = torch.zeros(
                self.mean.shape[-1], self.mean.shape[-1], self.kernel.shape[0], self.kernel.shape[0]
            )
            # The last two dimensions represent the pairwise covariances between the test points
            # The first two dimensions represent the covariances between the classes for each pair of test points.
        except RuntimeError:
            self.mean = labels
            self.covariance_matrix = kernel

    def add_jitter(self, jitter: float = 1e-3):
        """
        Adds a small constant diagonal to the covariance matrix for numerical stability.

        :param jitter: The size of the constant diagonal.
        :return: The instance with the updated covariance matrix.
        """
        jitter_matrix = torch.eye(self.covariance_matrix.shape[-1]) * jitter
        jitter_matrix = jitter_matrix.unsqueeze(0).unsqueeze(0).expand(self.covariance_matrix.shape)

        assert jitter_matrix.shape == self.covariance_matrix.shape
        # Add jitter to the diagonal elements
        self.covariance_matrix += jitter_matrix
        return self


class InertKernelModel(ExactGPModel):
    """
    An inert model wrapping a kernel matrix.

    Uses a given kernel for prior and posterior and returns a dummy distribution holding the
    kernel matrix.
    """

    def __init__(
        self,
        train_inputs: Optional[torch.Tensor],
        train_targets: Optional[torch.Tensor],
        covar_module: gpytorch.kernels.Kernel,
        mean_module: Optional[gpytorch.means.Mean],
        likelihood: gpytorch.likelihoods.Likelihood,
        num_classes: int,
        **_: Any,
    ) -> None:
        """
        Initialise self.

        Note that while arbitrary keyword arguments are accepted, they are not inspected or used. This is to allow
        passing keyword parameters that are required by other GP models (e.g. `rng`) without raising a `TypeError`,
        which allows more generic code.

        :param train_inputs: (n_samples, n_features) The training inputs (features).
        :param train_targets: (n_samples,) The training targets (response).
        :param covar_module:  The prior kernel function to use.
        :param mean_module: Not used, remaining in the signature for compatibility.
        :param likelihood:  Likelihood to use with model.
        :param num_classes: The number of classes to use.
        """
        super(ExactGP, self).__init__()

        if train_inputs is None:
            self.train_inputs = None
            self.train_targets = None
        else:
            if torch.is_tensor(train_inputs):
                train_inputs = (train_inputs,)
            try:
                self.train_inputs = tuple(tri.unsqueeze(-1) if tri.ndimension() == 1 else tri for tri in train_inputs)
            except AttributeError as exc:
                raise TypeError("Train inputs must be a tensor, or a list/tuple of tensors") from exc
            self.train_targets = train_targets

        self.prediction_strategy = None
        self.n_classes = num_classes
        self.covar_module = covar_module
        self.mean_module = ZeroMean()
        self.likelihood = likelihood

    def train(self, mode: bool = True) -> ExactGPModel:
        """Set to training mode, if data is not None."""
        if mode is True and (self.train_inputs is None or self.train_targets is None):
            raise RuntimeError(
                "train_inputs, train_targets cannot be None in training mode. "
                "Call .eval() for prior predictions, or call .set_train_data() to add training data."
            )
        return super().train(mode)

    def _label_tensor(self, targets: torch.Tensor) -> LinearOperator:
        return DiagLinearOperator(torch.ones(self.n_classes))[targets.long()]

    @override
    def __call__(self, *args: Any, **kwargs: Any) -> DummyKernelDistribution:
        """Perform training or inference, depending on the current mode."""
        # TODO: Why do we accept variable numbers of arguments here? It seems to throw errors if you provide too many
        #  arguments, and the GPyTorch documentation seems very thin here. Also, `kwargs` is ignored entirely.
        # https://github.com/gchq/Vanguard/issues/292
        train_inputs = list(self.train_inputs) if self.train_inputs is not None else []
        inputs = [arg.unsqueeze(-1) if arg.ndimension() == 1 else arg for arg in args]

        input_equals_training_inputs = all(
            torch.equal(train_input, input) for train_input, input in zip(train_inputs, inputs)
        )

        if self.training:
            if settings.debug.on() and not input_equals_training_inputs:
                raise RuntimeError("You must train on the training inputs!")
            kernel_matrix = self.covar_module(*inputs)

        elif settings.prior_mode.on() or self.train_inputs is None or self.train_targets is None:
            # TODO: Prior mode evaluation fails due to a shape mismatch, seemingly due to the reference to
            #  train_targets in the return value.
            # https://github.com/gchq/Vanguard/issues/291
            kernel_matrix = self.covar_module(*args)

        else:
            if settings.debug.on() and input_equals_training_inputs:
                warnings.warn(
                    "The input matches the stored training data. Did you forget to call model.train()?",
                    GPInputWarning,
                )

            kernel_matrix = self.covar_module(*inputs, *train_inputs)

        # TODO: This will fail if train_targets is None. (AttributeError: 'NoneType' object has no attribute 'long')
        # https://github.com/gchq/Vanguard/issues/291
        labels = self._label_tensor(self.train_targets)
        assert labels.shape == torch.Size([kernel_matrix.shape[-1], self.n_classes])
        assert kernel_matrix.shape == torch.Size([inputs[0].shape[0], train_inputs[0].shape[0]])
        return DummyKernelDistribution(labels=labels, kernel=kernel_matrix)
