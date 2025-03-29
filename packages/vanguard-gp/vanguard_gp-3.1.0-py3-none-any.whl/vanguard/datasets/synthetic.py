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
Synthetic data is particularly useful when running tests, as the data can be specifically cultivated for one's needs.
"""

from collections.abc import Iterable
from typing import Callable, Optional, Union

import numpy as np
import torch
from numpy.typing import NDArray
from sklearn.preprocessing import StandardScaler

from vanguard import utils
from vanguard.datasets.basedataset import Dataset


def simple_f(x: NDArray[np.floating]) -> NDArray[np.floating]:
    r"""
    Map values through a simple equation.

    .. math::
        f(x) = \sin(2\pi x)
    """
    return np.sin(2 * np.pi * x)


def complicated_f(x: NDArray[np.floating]) -> NDArray[np.floating]:
    r"""
    Map values through a complicated equation.

    .. math::
        f(x) = -x^\frac{3}{2} + x\sin^2(2\pi x)
    """
    return -(x ** (3 / 2)) + x * simple_f(x) ** 2


def very_complicated_f(x: NDArray[np.floating]) -> NDArray[np.floating]:
    r"""
    Map values through a *very* complicated equation.

    .. math::
        f(x) = -x^\frac{3}{2} + x\sin^2(2\pi x) + x^2 \cos(10\pi x)
    """
    return complicated_f(x) + x**2 * np.cos(10 * np.pi * x)


class SyntheticDataset(Dataset):
    """
    Synthetic data with homoskedastic noise for testing.

    :param functions: The functions to be used to generate the synthetic data. If multiple functions are given,
        a multidimensional output is generated.
    :param output_noise: The standard deviation for the output standard deviation, defaults to 0.1. Only applied
        to the training data; the testing data has no output noise actually applied, but we still set
        `test_y_std = output_noise`.
    :param train_input_noise_bounds: The lower, upper bounds of the linearly varying noise
        for the training input. Defaults to (0.01, 0.05).
    :param test_input_noise_bounds: The lower, upper bounds of the linearly varying noise
        for the testing input. Defaults to (0.01, 0.03).
    :param n_train_points: The total number of training points.
    :param n_test_points: The total number of testing points.
    :param significance: The significance to be used.
    :param rng: Generator instance used to generate random numbers.
    """

    def __init__(
        self,
        functions: Iterable[Callable[[NDArray[np.floating]], NDArray[np.floating]]] = (simple_f,),
        output_noise: float = 0.1,
        train_input_noise_bounds: tuple[float, float] = (0.01, 0.05),
        test_input_noise_bounds: tuple[float, float] = (0.01, 0.03),
        n_train_points: int = 30,
        n_test_points: int = 50,
        significance: float = 0.025,
        rng: Optional[np.random.Generator] = None,
    ) -> None:
        """Initialise self."""
        self.functions = list(functions)

        self.rng = utils.optional_random_generator(rng)

        train_data = self.make_sample_data(n_train_points, train_input_noise_bounds, output_noise)
        test_data = self.make_sample_data(n_test_points, test_input_noise_bounds, 0)

        (train_x, train_x_std), train_y = train_data
        (test_x, test_x_std), test_y = test_data

        train_y_std = output_noise
        test_y_std = output_noise

        super().__init__(
            train_x, train_x_std, train_y, train_y_std, test_x, test_x_std, test_y, test_y_std, significance
        )

    def make_sample_data(
        self,
        n_points: int,
        input_noise_bounds: tuple[float, float],
        output_noise_level: Union[int, float],
        interval_length: float = 1,
    ) -> tuple[tuple[NDArray[np.floating], NDArray[np.floating]], NDArray[np.floating]]:
        """
        Create some sample data.

        :param n_points: The number of points to create.
        :param input_noise_bounds: The lower, upper bounds for the resulting input noise.
        :param output_noise_level: The amount of noise applied to the outputs.
        :param interval_length: Use to scale the exact image of the function, defaults to 1.
        :return: The output and the mean and standard deviation of the input, in the form ``(x_mean, x_std), y``.
        """
        x_mean = np.linspace(0, interval_length, n_points)
        x_std = np.linspace(*input_noise_bounds, n_points)

        individual_ys = []
        for function in self.functions:
            exact_y = function(x_mean * 2 / interval_length)
            y_noise = self.rng.normal(size=x_mean.shape) * output_noise_level
            y = exact_y + y_noise
            individual_ys.append(y)

        y = np.squeeze(np.stack(individual_ys, axis=-1))

        scaler = StandardScaler()
        x_mean = scaler.fit_transform(x_mean.reshape(-1, 1))
        x_std = x_std.reshape(-1, 1) / scaler.scale_
        return (x_mean, x_std), y


class MultidimensionalSyntheticDataset(Dataset):
    """
    Synthetic data with multiple input dimensions.

    :param functions: The functions used on each input dimension
        (they are combined linearly to make a single output).
    :param output_noise: The standard deviation for the output standard deviation, defaults to 0.1. Only applied
        to the training data; the testing data has no output noise actually applied, but we still set
        `test_y_std = output_noise`.
    :param train_input_noise_bounds: The lower, upper bounds of the linearly varying noise
        for the training input. Defaults to (0.01, 0.05).
    :param test_input_noise_bounds: The lower, upper bounds of the linearly varying noise
        for the testing input. Defaults to (0.01, 0.03).
    :param n_train_points: The total number of training points.
    :param n_test_points: The total number of testing points.
    :param significance: The significance to be used.
    :param rng: Generator instance used to generate random numbers.
    """

    def __init__(
        self,
        functions: Iterable[Callable[[NDArray[np.floating]], NDArray[np.floating]]] = (simple_f, complicated_f),
        output_noise: float = 0.1,
        train_input_noise_bounds: tuple[float, float] = (0.01, 0.05),
        test_input_noise_bounds: tuple[float, float] = (0.01, 0.03),
        n_train_points: int = 30,
        n_test_points: int = 50,
        significance: float = 0.025,
        rng: Optional[np.random.Generator] = None,
    ) -> None:
        """Initialise self."""
        rng = utils.optional_random_generator(rng)

        one_dimensional_datasets = [
            SyntheticDataset(
                functions=(function,),
                rng=rng,
                output_noise=output_noise,
                train_input_noise_bounds=train_input_noise_bounds,
                test_input_noise_bounds=test_input_noise_bounds,
                n_train_points=n_train_points,
                n_test_points=n_test_points,
                significance=significance,
            )
            for function in functions
        ]

        train_x = torch.stack([dataset.train_x.ravel() for dataset in one_dimensional_datasets], -1)
        train_x_std = torch.stack([dataset.train_x_std.ravel() for dataset in one_dimensional_datasets], -1)
        train_y = torch.mean(torch.stack([dataset.train_y.ravel() for dataset in one_dimensional_datasets], -1), dim=-1)
        train_y_std = one_dimensional_datasets[0].train_y_std

        test_x = torch.stack([dataset.test_x.ravel() for dataset in one_dimensional_datasets], -1)
        test_x_std = torch.stack([dataset.test_x_std.ravel() for dataset in one_dimensional_datasets], -1)
        test_y = torch.mean(torch.stack([dataset.test_y.ravel() for dataset in one_dimensional_datasets], -1), dim=-1)
        test_y_std = one_dimensional_datasets[0].test_y_std

        super().__init__(
            train_x, train_x_std, train_y, train_y_std, test_x, test_x_std, test_y, test_y_std, significance
        )


class HeteroskedasticSyntheticDataset(SyntheticDataset):
    """
    Synthetic data with heteroskedastic noise for testing.

    The ``train_y_std`` and ``test_y_std`` attributes are created by drawing from a normal distribution centred
    on the value of the ``output_noise`` parameter.

    :param functions: The functions to be used to generate the synthetic data.
    :param output_noise_mean: The mean for the output standard deviation, defaults to 0.1.
    :param output_noise_std: The standard deviation for the output standard deviation, defaults to 0.01.
    :param train_input_noise_bounds: The lower, upper bounds of the linearly varying noise
        for the training input. Defaults to (0.01, 0.05).
    :param test_input_noise_bounds: The lower, upper bounds of the linearly varying noise
        for the testing input. Defaults to (0.01, 0.03).
    :param n_train_points: The total number of training points.
    :param n_test_points: The total number of testing points.
    :param significance: The significance to be used.
    :param rng: Generator instance used to generate random numbers.
    """

    def __init__(
        self,
        functions: Iterable[Callable[[NDArray[np.floating]], NDArray[np.floating]]] = (simple_f,),
        output_noise_mean: float = 0.1,
        output_noise_std: float = 0.01,
        train_input_noise_bounds: tuple[float, float] = (0.01, 0.05),
        test_input_noise_bounds: tuple[float, float] = (0.01, 0.03),
        n_train_points: int = 30,
        n_test_points: int = 50,
        significance: float = 0.025,
        rng: Optional[np.random.Generator] = None,
    ) -> None:
        """Initialise self."""
        rng = utils.optional_random_generator(rng)
        super().__init__(
            functions,
            output_noise_mean,
            train_input_noise_bounds,
            test_input_noise_bounds,
            n_train_points,
            n_test_points,
            significance,
            rng=rng,
        )

        # Slightly hacky conversion of numpy generator to torch generator
        torch_rng = torch.Generator(device=self.train_x.device).manual_seed(self.rng.integers(2**32).item())
        self.train_y_std = torch.normal(self.train_y_std, output_noise_std, generator=torch_rng).clamp(min=0)
        self.test_y_std = torch.normal(self.test_y_std, output_noise_std, generator=torch_rng).clamp(min=0)


class HigherRankSyntheticDataset(Dataset):
    """
    Synthetic data with rank 2 input features. In this case each x is a 2x2 matrix.

    :param functions: The functions to be used to generate the synthetic data.
    :param output_noise: The standard deviation for the output standard deviation, defaults to 0.1.
    :param train_input_noise_bounds: The lower, upper bounds of the linearly varying noise
        for the training input. Defaults to (0.01, 0.05).
    :param test_input_noise_bounds: The lower, upper bounds of the linearly varying noise
        for the testing input. Defaults to (0.01, 0.03).
    :param n_train_points: The total number of training points.
    :param n_test_points: The total number of testing points.
    :param significance: The significance to be used.
    :param rng: Generator instance used to generate random numbers.
    """

    def __init__(
        self,
        functions: Iterable[Callable[[NDArray[np.floating]], NDArray[np.floating]]] = (simple_f,),
        output_noise: float = 0.1,
        train_input_noise_bounds: tuple[float, float] = (0.01, 0.05),
        test_input_noise_bounds: tuple[float, float] = (0.01, 0.03),
        n_train_points: int = 30,
        n_test_points: int = 50,
        significance: float = 0.025,
        rng: Optional[np.random.Generator] = None,
    ) -> None:
        """Initialise self."""
        self.functions = list(functions)

        self.rng = utils.optional_random_generator(rng)

        train_data = self.make_sample_data(n_train_points, train_input_noise_bounds, output_noise)
        test_data = self.make_sample_data(n_test_points, test_input_noise_bounds, 0)

        (train_x, train_x_std), train_y = train_data
        (test_x, test_x_std), test_y = test_data

        train_y_std = output_noise
        test_y_std = output_noise

        super().__init__(
            train_x, train_x_std, train_y, train_y_std, test_x, test_x_std, test_y, test_y_std, significance
        )

    def make_sample_data(
        self,
        n_points: int,
        input_noise_bounds: tuple[float, float],
        output_noise_level: Union[int, float],
        interval_length: float = 1,
    ) -> tuple[tuple[NDArray[np.floating], NDArray[np.floating]], NDArray[np.floating]]:
        """
        Create some sample data.

        :param n_points: The number of points to create.
        :param input_noise_bounds: The lower, upper bounds for the resulting input noise.
        :param output_noise_level: The amount of noise applied to the inputs.
        :param interval_length: Use to scale the exact image of the function, defaults to 1.
        :return: The output and the mean and standard deviation of the input, in the form ``(x_mean, x_std), y``.
        """
        # Pylint is getting a false positive from `reshape` twice here
        x_mean = np.linspace(0, interval_length, n_points)
        x_mean = self.rng.standard_normal((n_points, 2, 2)) + x_mean.reshape((-1, 1, 1))

        x_std = np.linspace(*input_noise_bounds, n_points)
        x_std = np.ones((n_points, 2, 2)) + x_std.reshape(-1, 1, 1)  # pylint: disable=too-many-function-args

        fixed_matrix = np.array([[1, 0.5], [0, 2]])

        individual_ys = []
        for function in self.functions:
            exact_y = function(x_mean @ fixed_matrix * 2 / interval_length).mean(axis=1).mean(axis=1)
            y_noise = self.rng.normal(size=x_mean.shape[0]) * output_noise_level
            y = exact_y + y_noise
            individual_ys.append(y)

        y = np.squeeze(np.stack(individual_ys, axis=-1))

        return (x_mean, x_std), y
