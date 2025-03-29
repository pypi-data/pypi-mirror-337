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
Contains some multitask classification likelihoods.
"""

from typing import Any, Optional, Union

import gpytorch.distributions
import numpy as np
import numpy.typing
import torch
from gpytorch import ExactMarginalLogLikelihood
from gpytorch.constraints import Interval, Positive
from gpytorch.likelihoods import BernoulliLikelihood
from gpytorch.likelihoods import SoftmaxLikelihood as _SoftmaxLikelihood
from gpytorch.likelihoods.likelihood import _OneDimensionalLikelihood
from gpytorch.likelihoods.noise_models import MultitaskHomoskedasticNoise
from gpytorch.priors import Prior
from linear_operator import LinearOperator
from linear_operator.operators import DiagLinearOperator
from torch import Tensor
from torch.distributions import Distribution
from typing_extensions import override

from vanguard.classification.models import DummyKernelDistribution


class DummyNoise:
    """
    Provides a dummy wrapper around a tensor so that the tensor can be accessed as the noise property of the class.
    """

    def __init__(self, value: Union[float, numpy.typing.NDArray[np.floating], Tensor]) -> None:
        """
        Initialise self.

        :param value: Always returned by the :attr:noise property.
        """
        self.value = value

    @property
    def noise(self) -> Union[float, numpy.typing.NDArray[np.floating], Tensor]:
        """Return the dummy noise value."""
        return self.value


class MultitaskBernoulliLikelihood(BernoulliLikelihood):
    """
    A very simple extension of :class:`gpytorch.likelihoods.BernoulliLikelihood`.

    Provides an improper likelihood over multiple independent Bernoulli distributions.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Initialise self and ignore the num_tasks kwarg that may be passed to multi-task likelihoods.
        """
        kwargs.pop("num_classes", None)
        kwargs.pop("num_tasks", None)
        super().__init__(*args, **kwargs)

    def log_marginal(
        self, observations: torch.Tensor, function_dist: gpytorch.distributions.Distribution, *args, **kwargs
    ):
        """Compute the log probability sum summing the log probabilities over the tasks."""
        # TODO: investigate why this works/why it's been missed that it doesn't work?
        # https://github.com/gchq/Vanguard/issues/218
        # pylint: disable=no-member
        return super().log_prob(observations, function_dist, *args, **kwargs).sum(dim=-1)

    def expected_log_prob(
        self, observations: torch.Tensor, function_dist: gpytorch.distributions.Distribution, *args, **kwargs
    ):
        """Compute the expected log probability sum summing the expected log probabilities over the tasks."""
        return super().expected_log_prob(observations, function_dist, *args, **kwargs).sum(dim=-1)


class SoftmaxLikelihood(_SoftmaxLikelihood):
    """
    Superficial wrapper around the GPyTorch :class:`gpytorch.likelihoods.SoftmaxLikelihood`.

    This wrapper allows the arg names more consistent with other likelihoods.
    """

    def __init__(
        self, *args: Any, num_classes: Optional[int] = None, num_tasks: Optional[int] = None, **kwargs: Any
    ) -> None:
        r"""
        Initialise self.

        :param args: For full signature, see :class:`gpytorch.likelihoods.SoftmaxLikelihood`.
        :param num_classes: The number of target classes.
        :param num_tasks: Dimensionality of latent function :math:`\mathbf f`.
        :param kwargs: For full signature, see :class:`gpytorch.likelihoods.SoftmaxLikelihood`.
        """
        super().__init__(*args, num_classes=num_classes, num_features=num_tasks, **kwargs)


class DirichletKernelDistribution(torch.distributions.Dirichlet):
    # pylint: disable=abstract-method
    """
    A pseudo Dirichlet distribution with the log probability modified.
    """

    def __init__(
        self,
        label_matrix: Union[torch.Tensor, LinearOperator],
        kernel_matrix: Union[torch.Tensor, LinearOperator],
        alpha: Union[torch.Tensor, float],
    ) -> None:
        """
        Initialise self.

        :param label_matrix: (``n_data_points``,``n_classes``) A binary indicator matrix encoding the class to which
                                                               each data point belongs.
        :param kernel_matrix: (``n_data_points``,``n_data_points``) The evaluated kernel matrix.
        :param alpha: (``n_classes``,) The Dirichlet prior concentration parameters.
        """
        self.label_matrix = label_matrix
        self.kernel_matrix = kernel_matrix
        self.alpha = alpha

        # In DirichletKernelMulticlassClassification of fuzzy points, in posterior-mode,
        # self.label_matrix.shape = [default_group_size, num_test_points, num_classes], and
        # self.kernel_matrix.shape = [default_group_size, num_classes, num_classes, num_test_points, num_test_points]
        # so the line below errors due to mismatched sizes
        concentration = (self.kernel_matrix @ self.label_matrix + torch.unsqueeze(self.alpha, 0)).to_dense()
        super().__init__(concentration)

    @override
    def log_prob(self, value: torch.Tensor) -> torch.Tensor:
        one_hot_values = DiagLinearOperator(torch.ones(self.label_matrix.shape[1]))[value.long()]
        all_class_grouped_kernel_entries = self.kernel_matrix @ one_hot_values + torch.unsqueeze(self.alpha, 0)
        relevant_logits = all_class_grouped_kernel_entries.to_dense().log() * one_hot_values.to_dense()
        partition_function = (self.alpha.sum() + self.kernel_matrix.sum(dim=-1)).log()
        return relevant_logits.sum() - partition_function.sum()


class DirichletKernelClassifierLikelihood(_OneDimensionalLikelihood):
    """
    A pseudo Dirichlet likelihood.
    """

    def __init__(
        self,
        num_classes: int,
        alpha: Optional[Union[float, numpy.typing.NDArray[np.floating]]] = None,
        learn_alpha: bool = False,
        alpha_prior: Optional[Prior] = None,
        alpha_constraint: Optional[Interval] = Positive(),
    ) -> None:
        """
        Initialise self.

        :param num_classes: The number of classes in the data.
        :param alpha: The Dirichlet prior concentration. If a float, this will be assumed homogenous.
        :param learn_alpha: If to learn the Dirichlet prior concentration as a parameter.
        :param alpha_prior: Only used if :param:learn_alpha = True. The noise prior to use when learning the Dirichlet
            prior concentration.
        :param alpha_constraint: Only used if :param:learn_alpha = True. The constraint to apply to the learned value
            of `alpha` for the Dirichlet prior concentration.
        """
        super().__init__()
        self.n_classes = num_classes
        if alpha is None:
            self._alpha_var = torch.ones(self.n_classes)
        else:
            self._alpha_var = torch.as_tensor(alpha) * torch.ones(self.n_classes)

        if learn_alpha:
            alpha_val = self._alpha_var.clone()
            self._alpha_var = MultitaskHomoskedasticNoise(
                num_classes, noise_constraint=alpha_constraint, noise_prior=alpha_prior
            )
            self._alpha_var.initialize(noise=alpha_val)
        else:
            self._alpha_var = DummyNoise(self._alpha_var)

    @property
    def alpha(self) -> Optional[Union[float, numpy.typing.NDArray[np.floating], Tensor]]:
        """Return the Dirichlet prior concentration :math:`\alpha`."""
        return self._alpha_var.noise

    @override
    # pylint: disable=arguments-differ
    def forward(self, function_samples: torch.Tensor, **kwargs) -> Distribution:
        """Not implemented, but a concrete implementation is required by the abstract base class."""
        raise NotImplementedError

    @override
    # pylint: disable=arguments-differ
    def log_marginal(
        self, observations: torch.Tensor, function_dist: DummyKernelDistribution, **kwargs
    ) -> torch.Tensor:
        marginal = self.marginal(function_dist, **kwargs)
        return marginal.log_prob(observations)

    @override
    def marginal(self, function_dist: DummyKernelDistribution, *args, **kwargs) -> DirichletKernelDistribution:
        return DirichletKernelDistribution(function_dist.labels, function_dist.kernel, self.alpha)

    @override
    # The parameter `input` is taken from superclass method, so we can't rename it here.
    # pylint: disable=redefined-builtin
    def __call__(
        self, input: Union[torch.Tensor, DummyKernelDistribution], *args, **kwargs
    ) -> torch.distributions.Distribution:
        is_conditional = torch.is_tensor(input)
        is_marginal = isinstance(input, DummyKernelDistribution)

        if is_conditional:
            return super().__call__(input, *args, **kwargs)
        elif is_marginal:
            return self.marginal(input, *args, **kwargs)
        else:
            raise TypeError(
                "Likelihoods expects a DummyKernelDistribution input to make marginal predictions, or a "
                f"torch.Tensor for conditional predictions. Got a {type(input).__name__}"
            )


class GenericExactMarginalLogLikelihood(ExactMarginalLogLikelihood):
    """
    A lightweight modification of :class:`gpytorch.mlls.ExactMarginalLogLikelihood`.

    This removes some RuntimeErrors that prevent use with non-Gaussian likelihoods even when it is possible to do so.
    """

    def __init__(
        self,
        likelihood: Union[gpytorch.likelihoods._GaussianLikelihoodBase, DirichletKernelClassifierLikelihood],
        model: gpytorch.models.ExactGP,
    ) -> None:
        """
        Initialise self.

        :param likelihood: The Gaussian likelihood for the model.
        :param model: The exact GP.
        """
        super(ExactMarginalLogLikelihood, self).__init__(likelihood, model)

    def forward(
        self, function_dist: gpytorch.distributions.MultivariateNormal, target: torch.Tensor, *params, **kwargs
    ) -> torch.Tensor:
        r"""
        Compute the MLL given :math:`p(\mathbf f)` and :math:`\mathbf y`.

        :param function_dist: :math:`p(\mathbf f)` the outputs of the latent function
            (the :obj:`gpytorch.models.ExactGP`).
        :param target: :math:`\mathbf y` The target values.
        :return: Exact MLL. Output shape corresponds to batch shape of the model/input data.
        """
        output = self.likelihood(function_dist, *params, **kwargs)
        log_prob_of_marginal = output.log_prob(target)
        res = self._add_other_terms(log_prob_of_marginal, params)

        num_data = target.size(-1)
        scaled_data = res.div_(num_data)
        return scaled_data
