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
Keep track of loss and other metrics when training.

Vanguard supports a number of metrics pre-attached and tracked to all
controller classes. These are calculated per iteration by the
:class:`MetricsTracker` class.
"""

import itertools
from collections.abc import Iterator
from contextlib import contextmanager
from typing import TYPE_CHECKING, Callable, Optional

if TYPE_CHECKING:
    import vanguard.base.basecontroller


class MetricsTracker:
    """
    Tracks metrics for a controller.

    .. warning::
            Passing ``lambda`` functions is discouraged, as each ``lambda``
            function will overwrite the previous. Instead, create distinct
            functions for your metric.

    :Example:
        >>> from vanguard.base.metrics import loss
        >>>
        >>> tracker = MetricsTracker(loss)
        >>> for loss_value in range(5):
        ...     tracker.run_metrics(float(loss_value), controller=None)
        >>> with tracker.print_metrics():
        ...     for loss_value in range(5):
        ...         tracker.run_metrics(float(loss_value), controller=None)
        iteration: 6, loss: 0.0
        iteration: 7, loss: 1.0
        iteration: 8, loss: 2.0
        iteration: 9, loss: 3.0
        iteration: 10, loss: 4.0
        >>> with tracker.print_metrics(every=2):
        ...     for loss_value in range(5):
        ...         tracker.run_metrics(float(loss_value), controller=None)
        iteration: 12, loss: 1.0
        iteration: 14, loss: 3.0
        >>> with tracker.print_metrics(every=2, format_string="loss: {loss}"):
        ...     for loss_value in range(5):
        ...         tracker.run_metrics(float(loss_value), controller=None)
        loss: 1.0
        loss: 3.0
    """

    def __init__(
        self,
        *metrics: Callable,
    ) -> None:
        """
        Initialise self.

        A metric takes the form of a function of (loss, controller) -> real number.
        The simplest and most obvious metric simply returns the loss value, e.g.
        see the function `vanguard.base.metrics.loss`.
        Other common examples might extract parameters from the controller, e.g.
        a kernel's lengthscale, and return that.
        """
        self._metric_outputs = {}
        self._iteration = 0

        self.add_metrics(*metrics)

        self._every = float("nan")
        self._print_format_string = ""
        self._counter = itertools.count(1)

    def __getitem__(self, item):
        return {metric.__name__: output_values[item] for metric, output_values in self._metric_outputs.items()}

    def __len__(self):
        return len(self._metric_outputs)

    @property
    def _default_format_string(self) -> str:
        """Get the default format string used for printing."""
        format_string_components = ["iteration: {iteration}"]
        for metric in self._metric_outputs:
            component = f"{metric.__name__}: {{{metric.__name__}}}"
            format_string_components.append(component)
        format_string = ", ".join(format_string_components)
        return format_string

    def reset(self) -> None:
        """Remove the stored metrics outputs and reset the iteration count."""
        self._metric_outputs = {metric: [] for metric in self._metric_outputs}
        self._iteration = 0

    def add_metrics(
        self,
        *metrics: Callable,
    ) -> None:
        """
        Add metrics to the tracker.

        See __init__ docstring for definition of metrics.
        """
        for metric in metrics:
            self._metric_outputs[metric] = [float("nan")] * self._iteration

    def run_metrics(
        self,
        loss_value: float,
        controller: Optional["vanguard.base.basecontroller.BaseGPController"],
        **additional_info,
    ) -> None:
        """
        Register the components of an iteration.

        Each metric in the tracker will be run on the arguments of this method,
        and then stored for future reference. Iterations do not need to be passed.
        Additional information passed as keyword arguments can be displayed to
        the user when combined with :meth:`print_metrics` and a
        customised format string.

        :param loss_value: The loss.
        :param controller: The controller instance.
        """
        self._iteration += 1

        for metric, outputs in self._metric_outputs.items():
            metric_value = metric(loss_value, controller)
            outputs.append(metric_value)
            additional_info[metric.__name__] = metric_value

        additional_info["iteration"] = self._iteration

        if next(self._counter) % self._every == 0:
            try:
                output_string = self._print_format_string.format(**additional_info)
            except KeyError as error:
                output_string = f"{loss_value} (Could not find values for {repr(error.args[0])})"
            print(output_string)

    @contextmanager
    def print_metrics(
        self,
        every: int = 1,
        format_string: Optional[str] = None,
    ) -> Iterator[None]:
        """
        Temporarily enabling printing the metrics within a context manager.

        :param every: How often to print the output. Does not start on the
            first iteration. Defaults to 1 (print always).
        :param format_string: Used to format the output. Keys passed here
            must match with information passed to the :meth:`run_metrics` method.
            If None, all metrics will be printed.
        """
        if format_string is None:
            format_string = self._default_format_string

        self._every = every
        self._print_format_string = format_string
        self._counter = itertools.count(1)
        try:
            yield
        finally:
            self._print_format_string = ""
            self._every = float("nan")


def loss(loss_value: float, controller: Optional["vanguard.base.basecontroller.BaseGPController"]) -> float:  # pylint: disable=unused-argument
    """Return the loss value."""
    return loss_value
