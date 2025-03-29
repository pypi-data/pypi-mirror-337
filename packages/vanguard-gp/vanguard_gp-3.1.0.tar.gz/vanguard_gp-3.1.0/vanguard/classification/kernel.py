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
Contains the DirichletKernelMulticlassClassification decorator.
"""

from typing import Any, TypeVar, Union

import numpy as np
import numpy.typing
import torch
from torch import Tensor
from typing_extensions import override

from vanguard import utils
from vanguard.base import GPController
from vanguard.classification.likelihoods import DirichletKernelClassifierLikelihood
from vanguard.classification.mixin import Classification, ClassificationMixin
from vanguard.classification.models import InertKernelModel
from vanguard.decoratorutils import Decorator, process_args, wraps_class
from vanguard.warnings import warn_experimental

ControllerT = TypeVar("ControllerT", bound=GPController)
SAMPLE_DIM, TASK_DIM = 0, 2


class DirichletKernelMulticlassClassification(Decorator):
    """
    Implements multiclass classification using a Dirichlet kernel method.

    Based on the paper :cite:`MacKenzie14`.


    .. warning::
        This decorator is EXPERIMENTAL. It may cause errors or give incorrect results, and may have breaking changes
        without warning.

    .. warning::
        Fuzzy classification (with `classify_fuzzy_points`) is not supported.

    :Example:
        >>> from gpytorch.kernels import RBFKernel, ScaleKernel
        >>> import numpy as np
        >>> from vanguard.classification.likelihoods import (DirichletKernelClassifierLikelihood,
        ...                                                  GenericExactMarginalLogLikelihood)
        >>> from vanguard.vanilla import GaussianGPController
        >>>
        >>> @DirichletKernelMulticlassClassification(num_classes=3, ignore_methods=("__init__",))
        ... class MulticlassClassifier(GaussianGPController):
        ...     pass
        >>>
        >>> class Kernel(ScaleKernel):
        ...     def __init__(self) -> None:
        ...         super().__init__(RBFKernel())
        >>>
        >>> train_x = np.array([0, 0.1, 0.45, 0.55, 0.9, 1])
        >>> train_y = np.array([0, 0, 1, 1, 2, 2])
        >>>
        >>> gp = MulticlassClassifier(train_x, train_y, Kernel, y_std=0.0,
        ...                           likelihood_class=DirichletKernelClassifierLikelihood,
        ...                           marginal_log_likelihood_class=GenericExactMarginalLogLikelihood)
        >>> loss = gp.fit(100)
        >>>
        >>> test_x = np.array([0.05, 0.5, 0.95])
        >>> predictions, probs = gp.classify_points(test_x)
        >>> predictions.tolist()
        [0, 1, 2]
    """

    def __init__(self, num_classes: int, **kwargs: Any) -> None:
        """
        Initialise self.

        :param num_classes: The number of target classes.
        :param kwargs: Keyword arguments passed to :class:`~vanguard.decoratorutils.basedecorator.Decorator`.
        """
        warn_experimental("The DirichletKernelMulticlassClassification decorator")
        self.num_classes = num_classes
        super().__init__(framework_class=GPController, required_decorators={}, **kwargs)

    @property
    @override
    def safe_updates(self) -> dict[type, set[str]]:
        # pylint: disable=import-outside-toplevel
        from vanguard.learning import LearnYNoise
        from vanguard.normalise import NormaliseY
        from vanguard.standardise import DisableStandardScaling
        from vanguard.variational import VariationalInference
        from vanguard.warps import SetInputWarp, SetWarp
        # pylint: enable=import-outside-toplevel

        return self._add_to_safe_updates(
            super().safe_updates,
            {
                VariationalInference: {"__init__", "_predictive_likelihood", "_fuzzy_predictive_likelihood"},
                DisableStandardScaling: {"_input_standardise_modules"},
                LearnYNoise: {"__init__"},
                NormaliseY: {"__init__", "warn_normalise_y"},
                SetInputWarp: {"__init__"},
                SetWarp: {"__init__", "_loss", "_sgd_round", "warn_normalise_y", "_unwarp_values"},
            },
        )

    def _decorate_class(self, cls: type[ControllerT]) -> type[ControllerT]:
        num_classes = self.num_classes

        @Classification(ignore_all=True)
        @wraps_class(cls, decorator_source=self)
        class InnerClass(cls, ClassificationMixin):
            gp_model_class = InertKernelModel

            def __init__(self, *args: Any, **kwargs: Any) -> None:
                all_parameters_as_kwargs = process_args(super().__init__, *args, **kwargs)
                self.rng = utils.optional_random_generator(all_parameters_as_kwargs.pop("rng", None))

                likelihood_class = all_parameters_as_kwargs.pop("likelihood_class")
                if not issubclass(likelihood_class, DirichletKernelClassifierLikelihood):
                    raise ValueError(
                        "The class passed to `likelihood_class` must be a subclass of "
                        f"{DirichletKernelClassifierLikelihood.__name__}."
                    )

                train_y = all_parameters_as_kwargs.pop("train_y")

                likelihood_kwargs = all_parameters_as_kwargs.pop("likelihood_kwargs", {})
                model_kwargs = all_parameters_as_kwargs.pop("gp_kwargs", {})

                targets = torch.as_tensor(train_y, device=self.device, dtype=torch.int64)
                likelihood_kwargs["targets"] = targets
                likelihood_kwargs["num_classes"] = num_classes
                model_kwargs["num_classes"] = num_classes

                super().__init__(
                    train_y=train_y,
                    likelihood_class=likelihood_class,
                    likelihood_kwargs=likelihood_kwargs,
                    gp_kwargs=model_kwargs,
                    rng=self.rng,
                    **all_parameters_as_kwargs,
                )

            def classify_points(
                self, x: Union[float, numpy.typing.NDArray[np.floating], Tensor]
            ) -> tuple[Tensor, Tensor]:
                """Classify points."""
                x = torch.as_tensor(x)
                means_as_floats, _ = super().predictive_likelihood(x).prediction()
                return self._get_predictions_from_prediction_means(means_as_floats)

            # TODO: original code throws an error - see linked issue
            # https://github.com/gchq/Vanguard/issues/288
            def classify_fuzzy_points(
                self,
                x: Union[float, numpy.typing.NDArray[np.floating], Tensor],
                x_std: Union[float, numpy.typing.NDArray[np.floating], Tensor],
            ) -> tuple[Tensor, Tensor]:
                """Classify fuzzy points - not supported for this class."""
                msg = "Fuzzy classification is not supported for DirichletKernelMulticlassClassification."
                raise NotImplementedError(msg)

            @staticmethod
            def _get_predictions_from_prediction_means(
                means: Union[float, numpy.typing.NDArray[np.floating], Tensor],
            ) -> tuple[Tensor, Tensor]:
                """
                Get the predictions and certainty probabilities from predictive likelihood means.

                :param means: The prediction means in the range [0, 1].
                :returns: The predicted class labels, and the certainty probabilities.
                """
                means = torch.as_tensor(means)
                certainty, prediction = torch.max(means, dim=1)
                return prediction, certainty

        return InnerClass
