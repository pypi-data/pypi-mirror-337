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
Contains decorators to deal with input features that aren't vectors.
"""

import warnings
from functools import partial
from typing import Any, TypeVar, Union

import numpy as np
import torch
from gpytorch.models import GP
from typing_extensions import override

from vanguard import utils
from vanguard.base import GPController
from vanguard.classification.mixin import Classification, ClassificationMixin
from vanguard.decoratorutils import Decorator, process_args, wraps_class
from vanguard.decoratorutils.basedecorator import T
from vanguard.decoratorutils.errors import BadCombinationWarning
from vanguard.variational import VariationalInference
from vanguard.warnings import warn_experimental

ControllerT = TypeVar("ControllerT", bound=GPController)
GPModelT = TypeVar("GPModelT", bound=GP)


class HigherRankFeatures(Decorator):
    """
    Make a :class:`~vanguard.base.gpcontroller.GPController` compatible with higher rank features.

    GPyTorch assumes that input features are rank-1 (vectors) and a variety of
    RuntimeErrors are thrown from different places in the code if this is not true.
    This decorator modifies the gp model class to make it compatible with higher
    rank features.

    .. warning::
        This decorator is EXPERIMENTAL. It may cause errors or give incorrect results, and may have breaking changes
        without warning.

    :Example:
        >>> @HigherRankFeatures(2)
        ... class NewController(GPController):
        ...     pass
    """

    def __init__(self, rank: int, **kwargs: Any) -> None:
        """
        :param rank: The rank of the input features. Should be a positive integer.
        """
        warn_experimental("The HigherRankFeatures decorator")
        super().__init__(framework_class=GPController, required_decorators={}, **kwargs)
        self.rank = rank

    @override
    def verify_decorated_class(self, cls: type[T]) -> None:
        super().verify_decorated_class(cls)

        decorators = getattr(cls, "__decorators__", [])
        if any(issubclass(decorator, HigherRankFeatures) for decorator in decorators):
            warnings.warn(
                "Multiple instances of `@HigherRankFeatures` not supported."
                " Please only apply one instance of `@HigherRankFeatures` at once.",
                BadCombinationWarning,
                stacklevel=3,
            )

    @property
    @override
    def safe_updates(self) -> dict[type, set[str]]:
        # pylint: disable=import-outside-toplevel
        from vanguard.classification import BinaryClassification
        from vanguard.learning import LearnYNoise
        from vanguard.normalise import NormaliseY
        from vanguard.standardise import DisableStandardScaling
        from vanguard.warps import SetInputWarp, SetWarp
        # pylint: enable=import-outside-toplevel

        return self._add_to_safe_updates(
            super().safe_updates,
            {
                ClassificationMixin: {"classify_points", "classify_fuzzy_points"},
                Classification: {
                    "posterior_over_point",
                    "posterior_over_fuzzy_point",
                    "fuzzy_predictive_likelihood",
                    "predictive_likelihood",
                },
                VariationalInference: {"__init__", "_predictive_likelihood", "_fuzzy_predictive_likelihood"},
                DisableStandardScaling: {"_input_standardise_modules"},
                LearnYNoise: {"__init__"},
                NormaliseY: {"__init__", "warn_normalise_y"},
                SetInputWarp: {"__init__"},
                SetWarp: {"__init__", "_loss", "_sgd_round", "warn_normalise_y", "_unwarp_values"},
                BinaryClassification: {
                    "__init__",
                    "classify_points",
                    "classify_fuzzy_points",
                    "_get_predictions_from_prediction_means",
                    "warn_normalise_y",
                },
            },
        )

    def _decorate_class(self, cls: type[ControllerT]) -> type[ControllerT]:
        rank = self.rank

        @wraps_class(cls, decorator_source=self)
        class InnerClass(cls):
            def __init__(self, *args: Any, **kwargs: Any) -> None:
                all_parameters_as_kwargs = process_args(super().__init__, *args, **kwargs)
                self.rng = utils.optional_random_generator(all_parameters_as_kwargs.pop("rng", None))
                train_x = all_parameters_as_kwargs["train_x"]
                self.gp_model_class = _HigherRankFeaturesModel(train_x.shape[-rank:])(self.gp_model_class)
                kernel_class = all_parameters_as_kwargs.pop("kernel_class")
                super().__init__(kernel_class=kernel_class, rng=self.rng, **all_parameters_as_kwargs)

        return InnerClass


class _HigherRankFeaturesModel:
    """
    A decorator for a model, enabling higher rank features.

    GPyTorch assumes that input features are rank-1 (vectors) and a variety of
    RuntimeErrors are thrown from different places in the code if this is not true.
    This decorator can be applied to a GPyTorch model and deals with the feature
    shapes to avoid these issues. The decorator intercepts the training data
    and any data passed to ``__call__``, flattening it so that the shapes work out
    correctly. The data are then returned to their native shape before any actual
    computation (e.g. inside kernels) is performed.
    """

    def __init__(self, shape: Union[tuple[int, ...], torch.Size]) -> None:
        """
        :param shape: The native shape of a single data point.
        """
        self.shape = tuple(shape)
        self.flat_shape = int(np.prod(self.shape))

    def __call__(self, model_cls: type[GPModelT]) -> type[GPModelT]:
        shape = self.shape
        flat_shape = self.flat_shape
        _flatten = partial(self._flatten, item_shape=shape, item_flat_shape=flat_shape)
        _unflatten = partial(self._unflatten, item_shape=shape)

        @wraps_class(model_cls)
        class InnerClass(model_cls):
            def __init__(self, train_x: torch.Tensor, *args: Any, **kwargs: Any) -> None:
                super().__init__(_flatten(train_x), *args, **kwargs)

            def __call__(self, *args, **kwargs):
                args = [_flatten(arg) for arg in args]
                return super().__call__(*args, **kwargs)

            def forward(self, x):
                return super().forward(_unflatten(x))

        return InnerClass

    @staticmethod
    def _flatten(tensor: torch.Tensor, item_shape: tuple[int, ...], item_flat_shape: int) -> torch.Tensor:
        """
        Reshapes tensors to flat (rank - 1) features.

        :param tensor: The tensor to reshape.
        :param item_shape: The native shape of a single item.
        :param item_flat_shape: The flatten length of a single item.

        :returns: Reshape tensor.
        """
        new_shape = tuple(tensor.shape[: -len(item_shape)])
        new_shape = new_shape + (item_flat_shape,)
        return tensor.reshape(new_shape)

    @staticmethod
    def _unflatten(tensor: torch.Tensor, item_shape: tuple[int, ...]) -> torch.Tensor:
        """
        Reshapes flatten tensors to native feature shape.

        :param tensor: The tensor to reshape.
        :param item_shape: The native shape of a single item.

        :returns: Reshape tensor.
        """
        new_shape = tuple(tensor.shape[:-1])
        new_shape = new_shape + item_shape
        return tensor.reshape(new_shape)
