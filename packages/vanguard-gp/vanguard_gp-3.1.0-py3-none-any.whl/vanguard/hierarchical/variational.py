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
Contains the VariationalHierarchicalHyperparameters decorator.
"""

from collections.abc import Generator
from typing import Any, Optional, TypeVar, Union

import gpytorch
import numpy as np
import torch
from gpytorch.variational import CholeskyVariationalDistribution, _VariationalDistribution
from linear_operator import to_linear_operator
from numpy.typing import NDArray
from torch import Tensor
from typing_extensions import override

from vanguard import utils
from vanguard.decoratorutils import process_args, wraps_class
from vanguard.hierarchical.base import (
    BaseHierarchicalHyperparameters,
    GPController,
    Posterior,
    extract_bayesian_hyperparameters,
    set_batch_shape,
)
from vanguard.hierarchical.collection import HyperparameterCollection
from vanguard.variational import VariationalInference

ControllerT = TypeVar("ControllerT", bound=GPController)
KernelT = TypeVar("KernelT", bound=gpytorch.kernels.Kernel)
LikelihoodT = TypeVar("LikelihoodT", bound=gpytorch.likelihoods.GaussianLikelihood)
PosteriorT = TypeVar("PosteriorT", bound=Posterior)
DistributionT = TypeVar("DistributionT", bound=gpytorch.distributions.Distribution)


class VariationalHierarchicalHyperparameters(BaseHierarchicalHyperparameters):
    """
    Convert a controller so that variational inference is performed over its hyperparameters.

    Note that only those hyperparameters specified using the
    :class:`~vanguard.hierarchical.module.BayesianHyperparameters` decorator will be included
    for variational inference. The remaining hyperparameters will be inferred as point estimates.

    :Example:
        >>> from gpytorch.kernels import RBFKernel
        >>> import numpy as np
        >>> import torch
        >>> import torch.random
        >>> from vanguard.vanilla import GaussianGPController
        >>> from vanguard.hierarchical import (BayesianHyperparameters,
        ...                                    VariationalHierarchicalHyperparameters)
        >>>
        >>> @VariationalHierarchicalHyperparameters(num_mc_samples=50)
        ... class HierarchicalController(GaussianGPController):
        ...     pass
        >>>
        >>> @BayesianHyperparameters()
        ... class BayesianRBFKernel(RBFKernel):
        ...     pass
        >>>
        >>> train_x = torch.tensor([0, 0.5, 0.9, 1])
        >>> rng = torch.Generator(device=train_x.device).manual_seed(1234)
        >>> train_y = torch.normal(mean=1 / (1 + train_x), std=torch.ones_like(train_x) * 0.005, generator=rng)
        >>> gp = HierarchicalController(train_x, train_y, BayesianRBFKernel, y_std=0.0)
        >>> loss = gp.fit(100)
        >>>
        >>> test_x = torch.tensor([0.05, 0.95])
        >>> mean, lower, upper = gp.posterior_over_point(test_x).confidence_interval()
        >>> (upper > 1/(1 + test_x)).all().item(), (lower < 1/(1 + test_x)).all().item()
        (True, True)
    """

    def __init__(
        self,
        num_mc_samples: int = 100,
        variational_distribution_class: Optional[_VariationalDistribution] = CholeskyVariationalDistribution,
        **kwargs: Any,
    ) -> None:
        """
        Initialise self.

        :param num_mc_samples: The number of Monte Carlo samples to use when approximating
                                    intractable integrals in the variational ELBO and the
                                    predictive posterior.
        :param variational_distribution_class:
            The variational distribution to use for the raw hyperparameters' posterior. Defaults
            to :class:`~gpytorch.variational.CholeskyVariationalDistribution`.
        """
        super().__init__(num_mc_samples=num_mc_samples, **kwargs)
        self.variational_distribution_class = variational_distribution_class

    @property
    @override
    def safe_updates(self) -> dict[type, set[str]]:
        # pylint: disable=import-outside-toplevel
        from vanguard.learning import LearnYNoise
        from vanguard.multitask import Multitask
        from vanguard.normalise import NormaliseY
        from vanguard.standardise import DisableStandardScaling
        from vanguard.warps import SetInputWarp, SetWarp
        # pylint: enable=import-outside-toplevel

        return self._add_to_safe_updates(
            super().safe_updates,
            {
                DisableStandardScaling: {"_input_standardise_modules"},
                LearnYNoise: {"__init__"},
                Multitask: {"__init__", "_match_mean_shape_to_kernel"},
                NormaliseY: {"__init__", "warn_normalise_y"},
                SetInputWarp: {"__init__"},
                SetWarp: {"__init__", "_loss", "_sgd_round", "warn_normalise_y", "_unwarp_values"},
                VariationalInference: {"__init__", "_predictive_likelihood", "_fuzzy_predictive_likelihood"},
            },
        )

    def _decorate_class(self, cls: type[ControllerT]) -> type[ControllerT]:
        sample_shape = self.sample_shape
        variational_distribution_class = self.variational_distribution_class
        base_decorated_cls = super()._decorate_class(cls)

        @wraps_class(base_decorated_cls, decorator_source=self)
        class InnerClass(base_decorated_cls):
            def __init__(self, *args: Any, **kwargs: Any) -> None:
                for module_name in ("kernel", "mean", "likelihood"):
                    set_batch_shape(kwargs, module_name, sample_shape)

                all_parameters_as_kwargs = process_args(super().__init__, *args, **kwargs)
                self.rng = utils.optional_random_generator(all_parameters_as_kwargs.pop("rng", None))
                # Pop `rng` from kwargs to ensure we don't provide duplicate values to superclass init
                kwargs.pop("rng", None)
                super().__init__(*args, rng=self.rng, **kwargs)

                module_hyperparameter_pairs, point_estimate_kernels = extract_bayesian_hyperparameters(self)
                _correct_point_estimate_shapes(point_estimate_kernels)

                self.hyperparameter_collection = HyperparameterCollection(
                    module_hyperparameter_pairs, sample_shape, variational_distribution_class
                )

                self._smart_optimiser.update_registered_module(self._gp)
                self._smart_optimiser.register_module(self.hyperparameter_collection.variational_distribution)

            def _loss(self, train_x: torch.Tensor, train_y: torch.Tensor) -> torch.Tensor:
                """Add KL term to loss and average over hyperparameter samples."""
                self.hyperparameter_collection.sample_and_update()
                nmll = super()._loss(train_x, train_y)
                return nmll.mean() + self.hyperparameter_collection.kl_term()

        return InnerClass

    @staticmethod
    def _infinite_posterior_samples(
        controller: ControllerT, x: Union[Tensor, NDArray[np.floating]]
    ) -> Generator[torch.Tensor, None, None]:
        """
        Yield posterior samples forever.

        :param controller: The controller from which to yield samples.
        :param x: (n_predictions, n_features) The predictive inputs.
        """
        tx = torch.as_tensor(x, dtype=torch.float32, device=controller.device)
        while True:
            controller.hyperparameter_collection.sample_and_update()
            # pylint: disable=protected-access
            output = _safe_index_batched_multivariate_normal(controller._gp_forward(x=tx).add_jitter(1e-3))
            yield from output

    @staticmethod
    def _infinite_fuzzy_posterior_samples(
        controller: ControllerT,
        x: Union[Tensor, NDArray[np.floating]],
        x_std: Union[Tensor, NDArray[np.floating], float],
    ) -> Generator[torch.Tensor, None, None]:
        """
        Yield fuzzy posterior samples forever.

        :param controller: The controller from which to yield samples.
        :param x: (n_predictions, n_features) The predictive inputs.
        :param x_std: The input noise standard deviations:

            * array_like[float]: (n_features,) The standard deviation per input dimension for the predictions,
            * float: Assume homoskedastic noise.
        """
        tx = torch.tensor(x, dtype=torch.float32, device=controller.device)
        # pylint: disable-next=protected-access
        tx_std = controller._process_x_std(std=x_std).to(controller.device)
        while True:
            controller.hyperparameter_collection.sample_and_update()
            # This cunning trick matches the sampled x shape to the MC samples batch shape.
            # The results is that each sample from output comes from independent x samples
            # and from independent variational posterior samples.
            sample_shape = controller.hyperparameter_collection.sample_shape + tx.shape
            x_sample = torch.randn(size=sample_shape, device=controller.device) * tx_std + tx
            # pylint: disable-next=protected-access
            output = _safe_index_batched_multivariate_normal(controller._gp_forward(x=x_sample).add_jitter(1e-3))
            yield from output

    @staticmethod
    def _infinite_likelihood_samples(
        controller: ControllerT, x: Union[Tensor, NDArray[np.floating]]
    ) -> Generator[torch.Tensor, None, None]:
        """
        Yield likelihood samples forever.

        :param controller: The controller from which to yield samples.
        :param x: (n_predictions, n_features) The predictive inputs.
        """
        tx = torch.as_tensor(x, dtype=torch.float32, device=controller.device)
        while True:
            controller.hyperparameter_collection.sample_and_update()
            # pylint: disable-next=protected-access
            output = _safe_index_batched_multivariate_normal(controller._gp_forward(x=tx).add_jitter(1e-3))
            for sample in output:
                # pylint: disable-next=protected-access
                shape = controller._decide_noise_shape(controller.posterior_class(sample), x=tx)
                noise = torch.zeros(shape, dtype=torch.float32, device=controller.device)
                # pylint: disable-next=protected-access
                likelihood_output = controller._likelihood(sample, noise=noise)
                yield likelihood_output

    @staticmethod
    def _infinite_fuzzy_likelihood_samples(
        controller: ControllerT,
        x: Union[Tensor, NDArray[np.floating]],
        x_std: Union[Tensor, NDArray[np.floating], float],
    ) -> Generator[torch.Tensor, None, None]:
        """
        Yield fuzzy likelihood samples forever.

        :param controller: The controller from which to yield samples.
        :param x: (n_predictions, n_features) The predictive inputs.
        :param x_std: The input noise standard deviations:

            * array_like[float]: (n_features,) The standard deviation per input dimension for the predictions,
            * float: Assume homoskedastic noise.
        """
        tx = torch.tensor(x, dtype=torch.float32, device=controller.device)
        # pylint: disable-next=protected-access
        tx_std = controller._process_x_std(x_std).to(controller.device)

        while True:
            controller.hyperparameter_collection.sample_and_update()
            # This cunning trick matches the sampled x shape to the MC samples batch shape.
            # The results is that each sample from output comes from independent x samples
            # and from independent variational posterior samples.
            sample_shape = controller.hyperparameter_collection.sample_shape + tx.shape
            x_sample = torch.randn(size=sample_shape, device=controller.device) * tx_std + tx
            # pylint: disable-next=protected-access
            output = _safe_index_batched_multivariate_normal(controller._gp_forward(x=x_sample).add_jitter(1e-3))
            for sample in output:
                # pylint: disable-next=protected-access
                shape = controller._decide_noise_shape(controller.posterior_class(sample), x=tx)
                noise = torch.zeros(shape, dtype=torch.float32, device=controller.device)
                # pylint: disable-next=protected-access
                likelihood_output = controller._likelihood(sample, noise=noise)
                yield likelihood_output


def _correct_point_estimate_shapes(point_estimate_kernels: list[KernelT]) -> None:
    """
    Adjust the shape of the constants of point estimate kernels.

    These will be incorrect due to how GPyTorch handles batch shapes.
    """
    for point_estimate_scale_kernel in point_estimate_kernels:
        delattr(point_estimate_scale_kernel, "raw_outputscale")
        point_estimate_scale_kernel.register_parameter(
            name="raw_outputscale", parameter=torch.nn.Parameter(torch.zeros([1]))
        )


def _safe_index_batched_multivariate_normal(
    distribution: DistributionT,
) -> Generator[DistributionT, None, None]:
    """
    Delazifies the batched covariance matrix and yields recreated non-batch normals.

    Indexing into the batch dimension of batch :class:`~gpytorch.distributions.MultivariateNormal`
    is somewhat brittle when the underlying covariance matrix is lazy (which happens when the covariance
    matrix is larger than an obscure threshold). Hopefully this will change, but for now, we will work
    around it. This function delazifies the batched covariance matrix and yields recreated non-batch
    normals using then relazified individual covariance matrices.

    Delazifying the batch covariance matrix doesn't cause any inefficiencies because the individual
    covariance matrices would be delazified later anyway. Relazifying the individual matrices just
    delays any Cholesky issues, which is good because we have handling for them downstream.
    """
    distribution_type = type(distribution)
    non_lazy_covariance_matrix = distribution.covariance_matrix
    for sub_mean, sub_covariance_matrix in zip(distribution.mean, non_lazy_covariance_matrix):
        yield distribution_type(sub_mean, to_linear_operator(sub_covariance_matrix))
