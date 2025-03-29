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
Enable Bayesian hyperparameters in a Gaussian process.

The :mod:`~vanguard.hierarchical` module contains decorators
to implement Bayesian treatment of hyperparameters using variational inference,
as seen in :cite:`Lalchand20`, as well as Laplace approximation
treatment.
"""

from vanguard.hierarchical.laplace import LaplaceHierarchicalHyperparameters
from vanguard.hierarchical.module import BayesianHyperparameters
from vanguard.hierarchical.variational import VariationalHierarchicalHyperparameters

__all__ = [
    "LaplaceHierarchicalHyperparameters",
    "BayesianHyperparameters",
    "VariationalHierarchicalHyperparameters",
]
