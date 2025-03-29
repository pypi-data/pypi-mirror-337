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
Contains the SetWarp decorator.
"""

from typing import Any, TypeVar, Union

import numpy as np
import numpy.typing
import torch
from torch import Tensor
from typing_extensions import Self, override

from vanguard import utils
from vanguard.base import GPController
from vanguard.base.posteriors import Posterior
from vanguard.decoratorutils import Decorator, process_args, wraps_class
from vanguard.warps.basefunction import WarpFunction
from vanguard.warps.intermediate import is_intermediate_warp_function

ControllerT = TypeVar("ControllerT", bound=GPController)


class SetWarp(Decorator):
    """
    Map a GP through a warp function.

    :Example:
            >>> from vanguard.base import GPController
            >>> from vanguard.warps.warpfunctions import BoxCoxWarpFunction
            >>>
            >>> @SetWarp(BoxCoxWarpFunction(1))
            ... class MyController(GPController):
            ...     pass
    """

    def __init__(self, warp_function: WarpFunction, **kwargs: Any):
        """
        Initialise self.

        :param warp_function: The warp function to be applied to the GP.
        :param kwargs: Keyword arguments passed to :class:`~vanguard.decoratorutils.basedecorator.Decorator`.
        """
        super().__init__(framework_class=GPController, required_decorators={}, **kwargs)
        self.warp_function = warp_function

    @property
    @override
    def safe_updates(self) -> dict[type, set[str]]:
        # pylint: disable=import-outside-toplevel
        from vanguard.classification import (
            BinaryClassification,
            CategoricalClassification,
            DirichletMulticlassClassification,
        )
        from vanguard.classification.mixin import Classification, ClassificationMixin
        from vanguard.features import HigherRankFeatures
        from vanguard.hierarchical import LaplaceHierarchicalHyperparameters, VariationalHierarchicalHyperparameters
        from vanguard.learning import LearnYNoise
        from vanguard.multitask import Multitask
        from vanguard.normalise import NormaliseY
        from vanguard.standardise import DisableStandardScaling
        from vanguard.variational import VariationalInference
        from vanguard.warps import SetInputWarp
        # pylint: enable=import-outside-toplevel

        return self._add_to_safe_updates(
            super().safe_updates,
            {
                BinaryClassification: {
                    "__init__",
                    "classify_points",
                    "classify_fuzzy_points",
                    "_get_predictions_from_prediction_means",
                    "warn_normalise_y",
                },
                CategoricalClassification: {
                    "__init__",
                    "classify_points",
                    "classify_fuzzy_points",
                    "_get_predictions_from_posterior",
                    "warn_normalise_y",
                },
                ClassificationMixin: {"classify_points", "classify_fuzzy_points"},
                Classification: {
                    "posterior_over_point",
                    "posterior_over_fuzzy_point",
                    "fuzzy_predictive_likelihood",
                    "predictive_likelihood",
                },
                DisableStandardScaling: {"_input_standardise_modules"},
                DirichletMulticlassClassification: {
                    "__init__",
                    "_loss",
                    "_noise_transform",
                    "classify_points",
                    "classify_fuzzy_points",
                    "_get_predictions_from_prediction_means",
                    "warn_normalise_y",
                },
                HigherRankFeatures: {"__init__"},
                LaplaceHierarchicalHyperparameters: {
                    "__init__",
                    "_compute_hyperparameter_laplace_approximation",
                    "_compute_loss_hessian",
                    "_fuzzy_predictive_likelihood",
                    "_get_posterior_over_fuzzy_point_in_eval_mode",
                    "_get_posterior_over_point",
                    "_gp_forward",
                    "_predictive_likelihood",
                    "_sample_and_set_hyperparameters",
                    "_sgd_round",
                    "_update_hyperparameter_posterior",
                    "auto_temperature",
                },
                LearnYNoise: {"__init__"},
                Multitask: {"__init__", "_match_mean_shape_to_kernel"},
                NormaliseY: {"__init__", "warn_normalise_y"},
                SetInputWarp: {"__init__"},
                SetWarp: {"__init__", "_loss", "_sgd_round", "warn_normalise_y", "_unwarp_values"},
                VariationalHierarchicalHyperparameters: {
                    "__init__",
                    "_fuzzy_predictive_likelihood",
                    "_get_posterior_over_fuzzy_point_in_eval_mode",
                    "_get_posterior_over_point",
                    "_gp_forward",
                    "_loss",
                    "_predictive_likelihood",
                },
                VariationalInference: {"__init__", "_predictive_likelihood", "_fuzzy_predictive_likelihood"},
            },
        )

    def _decorate_class(self, cls: type[ControllerT]) -> type[ControllerT]:
        warp_function = self.warp_function

        @wraps_class(cls, decorator_source=self)
        class InnerClass(cls):
            """
            A wrapper for applying a compositional warp to a controller class.
            """

            def __init__(self, *args: Any, **kwargs: Any):
                all_parameters_as_kwargs = process_args(super().__init__, *args, **kwargs)
                self.rng = utils.optional_random_generator(all_parameters_as_kwargs.pop("rng", None))
                # Pop `rng` from kwargs to ensure we don't provide duplicate values to superclass
                kwargs.pop("rng", None)

                super().__init__(*args, rng=self.rng, **kwargs)

                for warp_component in warp_function.components:
                    if is_intermediate_warp_function(warp_component):
                        warp_component.activate(**all_parameters_as_kwargs)

                warp_copy = warp_function.copy().float()
                self.warp = warp_copy
                self._smart_optimiser.register_module(self.warp)
                self.train_y = self.train_y.to(self.device)

                def _unwarp_values(
                    *values: Union[Tensor, numpy.typing.NDArray[np.floating]],
                ) -> tuple[Tensor, ...]:
                    """
                    Map values back through the warp.

                    :param values: Values to reverse warping on
                    :return: Values warped back onto original space
                    """
                    values_as_tensors = (
                        torch.as_tensor(value, dtype=self.dtype, device=self.device) for value in values
                    )
                    unwarped_values_as_tensors = (warp_copy.inverse(tensor).squeeze() for tensor in values_as_tensors)
                    return tuple(unwarped_values_as_tensors)

                def _warp_values(
                    *values: Union[Tensor, numpy.typing.NDArray[np.floating]],
                ) -> tuple[Tensor, ...]:
                    """
                    Map values through the warp.

                    :param values: Values to warp on
                    :return: Values warp onto new space
                    """
                    values_as_tensors = (
                        torch.as_tensor(value, dtype=self.dtype, device=self.device) for value in values
                    )
                    warped_values_as_tensors = (warp_copy(tensor).squeeze() for tensor in values_as_tensors)
                    return tuple(warped_values_as_tensors)

                def _warp_derivative_values(
                    *values: Union[Tensor, numpy.typing.NDArray[np.floating]],
                ) -> tuple[Tensor, ...]:
                    """
                    Map values through the derivative of the warp.

                    :param values: Values to compute derivatives of warp for
                    :return: Derivatives of warp for each input value
                    """
                    values_as_tensors = (
                        torch.as_tensor(value, dtype=self.dtype, device=self.device) for value in values
                    )
                    warped_values_as_tensors = (warp_copy.deriv(tensor).squeeze() for tensor in values_as_tensors)
                    return tuple(warped_values_as_tensors)

                def warp_posterior_class(posterior_class: type[Posterior]) -> type[Posterior]:
                    """Wrap a posterior class to enable warping."""

                    @wraps_class(posterior_class)
                    class WarpedPosterior(posterior_class):
                        """
                        Un-scale the distribution at initialisation.
                        """

                        def prediction(self) -> torch.tensor:  # pytest: ignore [reportGeneralTypeIssues]
                            """Un-warp values."""
                            raise TypeError("The mean and covariance of a warped GP cannot be computed exactly.")

                        def confidence_interval(
                            self, alpha: float = 0.05
                        ) -> tuple[
                            numpy.typing.NDArray[np.floating],
                            numpy.typing.NDArray[np.floating],
                            numpy.typing.NDArray[np.floating],
                        ]:
                            """Un-warp values."""
                            mean, lower, upper = super().confidence_interval(alpha)
                            return _unwarp_values(mean, lower, upper)

                        def log_probability(
                            self, y: tuple[numpy.typing.NDArray[np.floating]]
                        ) -> numpy.typing.NDArray[np.floating]:
                            """Apply the change of variables to the density using the warp."""
                            warped_y = _warp_values(y)
                            warp_deriv_values = _warp_derivative_values(y)
                            jacobian = np.sum(np.log(np.abs(warp_deriv_values)))
                            return jacobian + super().log_probability(warped_y)

                    return WarpedPosterior

                self.posterior_class = warp_posterior_class(self.posterior_class)
                self.posterior_collection_class = warp_posterior_class(self.posterior_collection_class)

            @classmethod
            def new(cls, instance: Self, **kwargs: Any) -> Self:
                """Also apply warping to the new instance."""
                new_instance = super().new(instance, **kwargs)
                new_instance.warp = instance.warp
                # pylint: disable=protected-access
                new_instance._gp.train_targets = new_instance.warp(new_instance._gp.train_targets).squeeze(dim=-1)
                return new_instance

            def _sgd_round(self, n_iters: int = 100, gradient_every: int = 100) -> torch.Tensor:
                """Calculate loss and warp train_y."""
                loss = super()._sgd_round(n_iters=n_iters, gradient_every=gradient_every)
                warped_train_y = self.warp(self.train_y).squeeze(dim=-1)
                self._gp.train_targets = warped_train_y
                return loss

            def _unwarp_values(self, *values: Union[Tensor, numpy.typing.NDArray[np.floating]]) -> tuple[Tensor, ...]:
                """Map values back through the warp."""
                values_as_tensors = (torch.as_tensor(value) for value in values)
                unwarped_values_as_tensors = (self.warp.inverse(tensor).reshape(-1) for tensor in values_as_tensors)
                return tuple(unwarped_values_as_tensors)

            def _loss(self, train_x: torch.Tensor, train_y: torch.Tensor) -> torch.Tensor:
                """Subtract additional derivative term from the mll."""
                warped_train_y = self.warp(train_y).squeeze(dim=-1)
                self._gp.train_targets = warped_train_y
                nmll = super()._loss(train_x, warped_train_y)
                return nmll - self.warp.deriv(train_y).squeeze(dim=-1).sum()

            @staticmethod
            def warn_normalise_y() -> None:
                """Override base warning because warping renders y normalisation unimportant."""

        return InnerClass
