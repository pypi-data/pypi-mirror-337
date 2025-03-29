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
Distribute training and prediction across multiple controllers.

A controller class decorated with the  :class:`~vanguard.distribute.decorator.Distributed` decorator
will make predictions by aggregating the predictions of several independent expert controllers.
"""

from vanguard.distribute.decorator import Distributed

__all__ = ["Distributed"]
