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
Contains base models for approximate inference.
"""

from typing import Any, Optional, Union

import numpy as np
import torch
from gpytorch.distributions import MultivariateNormal
from gpytorch.kernels import Kernel
from gpytorch.likelihoods import Likelihood
from gpytorch.means import Mean
from gpytorch.models import ApproximateGP
from gpytorch.variational import (
    CholeskyVariationalDistribution,
    VariationalStrategy,
    _VariationalDistribution,
    _VariationalStrategy,
)
from numpy.typing import NDArray
from torch import Tensor

from vanguard import utils
from vanguard.decoratorutils.wrapping import wraps_class


class SVGPModel(ApproximateGP):
    """
    A standard model for approximate inference.

    GPyTorch approximate GP model subclassing :class:`gpytorch.models.ApproximateGP`
    with flexible prior kernel, mean and an inducing point variational approximation
    to the posterior al la :cite:`Hensman15`.
    """

    if torch.cuda.is_available():
        device = torch.device("cuda:0")
    else:
        device = torch.device("cpu")

    def __init__(
        self,
        train_x: Union[Tensor, NDArray[np.floating]],
        train_y: Union[Tensor, NDArray[np.floating]],  # pylint: disable=unused-argument
        likelihood: Likelihood,
        mean_module: Mean,
        covar_module: Kernel,
        n_inducing_points: int,
        rng: Optional[np.random.Generator] = None,
        **_: Any,
    ) -> None:
        """
        Initialise self.

        Note that while arbitrary keyword arguments are accepted, they are not inspected or used. This is to allow
        passing keyword parameters that are required by other GP models (e.g. `rng`) without raising a `TypeError`,
        which allows more generic code.

        :param train_x: (n_samples, n_features) The training inputs (features).
        :param train_y: (n_samples,) The training targets (response). Note that these are not used for this method!
            They are only passed here to match the `__init__()` signature of the other Vanguard GP models.
        :param likelihood:  Likelihood to use with model. Included only for signature consistency.
        :param mean_module: The prior mean function to use.
        :param covar_module:  The prior kernel function to use.
        :param n_inducing_points: The number of inducing points in the variational sparse kernel approximation.
        :param rng: Generator instance used to generate random numbers.
        """
        self.rng = utils.optional_random_generator(rng)
        self._check_batch_shape(mean_module, covar_module)

        train_x = torch.as_tensor(train_x)

        inducing_points = self._init_inducing_points(train_x, n_inducing_points)
        variational_distribution = self._build_variational_distribution(n_inducing_points)
        base_variational_strategy = self._build_base_variational_strategy(inducing_points, variational_distribution)
        variational_strategy = self._build_variational_strategy(base_variational_strategy)
        variational_strategy_class = type(variational_strategy)

        @wraps_class(variational_strategy_class)
        class SafeVariationalStrategy(variational_strategy_class):
            """A temporary class which will raise an appropriate error when the __call__ method fails."""

            def __call__(self, *args: Any, **kwargs: Any) -> MultivariateNormal:
                try:
                    return super().__call__(*args, **kwargs)
                except RuntimeError as exc:
                    cls = type(self)
                    full_path = ".".join((cls.__module__, cls.__qualname__))
                    if __debug__:
                        raise RuntimeError(
                            f"{full_path} may not be the correct choice for a variational strategy."
                        ) from exc
                    else:
                        raise RuntimeError(
                            "Unexpected Runtime Error! Potentially incorrect variational strategy."
                        ) from exc

        variational_strategy.__class__ = SafeVariationalStrategy
        super().__init__(variational_strategy)

        self.mean_module = mean_module
        self.covar_module = covar_module
        self.likelihood = likelihood

    def forward(self, x: Tensor) -> MultivariateNormal:
        """
        Compute the prior latent distribution on a given input.

        :param x: (n_samples, n_features) The inputs.
        :returns: The prior distribution.
        """
        mean_x = self.mean_module(x)
        covar_x = self.covar_module(x)
        return MultivariateNormal(mean_x, covar_x)

    def _init_inducing_points(self, train_x: Tensor, n_inducing_points: int) -> Tensor:
        """
        Create the initial inducing points by sampling from the training inputs.

        :param train_x: (n_training_points, n_features)
        :param n_inducing_points: How many inducing points to select.
        :returns: The inducing points sampled from the training points.
        """
        induce_indices = self.rng.choice(train_x.shape[0], size=n_inducing_points, replace=True)
        inducing_points = train_x[induce_indices]
        return inducing_points.to(self.device)

    def _build_variational_strategy(self, base_variational_strategy: _VariationalStrategy) -> _VariationalStrategy:
        """
        Construct the final variational strategy from the intermediate strategy.

        :param base_variational_strategy: The intermediate strategy.
        :returns: The final variational strategy to use.
        """
        return base_variational_strategy

    def _build_variational_distribution(self, n_inducing_points: int) -> _VariationalDistribution:
        """
        Construct the variational distribution.

        :param n_inducing_points: How many inducing points to use in the approximation.
        :returns: The variational distribution.
        """
        return CholeskyVariationalDistribution(n_inducing_points)

    def _build_base_variational_strategy(
        self, inducing_points: Tensor, variational_distribution: _VariationalDistribution
    ) -> _VariationalStrategy:
        """
        Build the base variational strategy.

        :param inducing_points: The inducing points sampled from the training points.
        :param variational_distribution: The variational distribution.
        :returns: The final variational strategy which will be used.
        """
        return VariationalStrategy(self, inducing_points, variational_distribution, learn_inducing_locations=True)

    # pylint: disable-next=unused-argument
    def _check_batch_shape(self, mean_module: Mean, covar_module: Kernel) -> None:
        """
        Ensure that the shapes are compatible.

        If data has an incorrect shape, the errors raised by mean/covar modules
        can be tricky to pinpoint back to batch shape problems. Since this is a
        common trap to fall into, we check for mistakes explicitly.
        """
        if hasattr(self, "num_tasks") and self.num_tasks != 1:
            raise TypeError(
                f"You are using a {SVGPModel.__name__} in a multi-task problem. {SVGPModel.__name__} does"
                f"not have the correct variational strategy for multi-task."
            )
