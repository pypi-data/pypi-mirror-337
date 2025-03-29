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
Wrapping functions for use in Vanguard decorators.

Applying the :func:`wraps_class` decorator to a class will
update all method names and docstrings with those of the super class. The
:func:`process_args` function is a helper function for organising arguments
to a function into a dictionary for straightforward access.
"""

import inspect
from functools import WRAPPER_ASSIGNMENTS, wraps
from typing import Any, Callable, Optional, TypeVar

from vanguard.decoratorutils import Decorator

T = TypeVar("T")


def process_args(func: Callable, *args: Any, **kwargs: Any) -> dict[str, Any]:
    """
    Process the arguments for a function.

    This is just a wrapper on :py:meth:`inspect.Signature.bind` that also applies any default arguments and folds any
    additional `kwargs` into the returned dictionary.

    Note that when passed a bound method, ``"self"`` will not be a key in the returned dictionary, and should not be
    passed as an argument (as a TypeError will be raised).

    Conversely, when passed an unbound method, ``"self"`` _must_ be passed as an argument if it's an instance method,
    and will be included in the returned dictionary.

    As such, if you need to use the result of applying this function on an unbound method as an argument list to a
    bound method, or vice versa, you'll have to handle the "self" parameter specially.

    :Example:
        >>> class MyClass:
        ...     def __init__(self, x: int):
        ...         self.x = x
        ...     def multiply(self, y: int) -> int:
        ...         return self.x * y
        >>> my_instance = MyClass(x=2)
        >>> process_args(my_instance.multiply, y=3)
        {'y': 3}
        >>> process_args(MyClass.multiply, y=3)
        Traceback (most recent call last):
        ...
        TypeError: missing a required argument: 'self'
        >>> process_args(MyClass.multiply, my_instance, y=3)  # doctest: +ELLIPSIS
        {'self': <...MyClass object at 0x...>, 'y': 3}

    :param func: The function for which to process the arguments.
    :param args: Arguments to be passed to the function. Must be passed as args,
                        i.e. ``process_args(func, 1, 2)``.
    :param kwargs: Keyword arguments to be passed to the function. Must be passed as kwargs,
                            i.e. ``process_args(func, c=1)``.

    :returns: A mapping of parameter name to value for all parameters (including default ones) of the function.

    :Example:
        >>> def f(a, b, c=3, **kwargs):
        ...     pass
        >>>
        >>> process_args(f, 1, 2)
        {'a': 1, 'b': 2, 'c': 3}
        >>> process_args(f, a=1, b=2, c=4)
        {'a': 1, 'b': 2, 'c': 4}
        >>> process_args(f, a=1, b=2, c=4, e=5)
        {'a': 1, 'b': 2, 'c': 4, 'e': 5}
        >>> process_args(f, *(1,), **{'b': 2, 'c': 4})
        {'a': 1, 'b': 2, 'c': 4}
        >>> process_args(f, 1)
        Traceback (most recent call last):
        ...
        TypeError: missing a required argument: 'b'
    """
    signature = inspect.signature(func)
    bound_args = signature.bind(*args, **kwargs)
    bound_args.apply_defaults()
    parameters_as_kwargs = bound_args.arguments
    inner_kwargs = parameters_as_kwargs.pop("kwargs", {})
    parameters_as_kwargs.update(inner_kwargs)

    return parameters_as_kwargs


def wraps_class(base_class: type[T], *, decorator_source: Optional[Decorator] = None) -> Callable[[type[T]], type[T]]:
    r"""
    Update the names and docstrings of an inner class to those of a base class.

    This decorator controls the wrapping of an inner class, ensuring that all
    methods of the final class maintain the same names and docstrings as the
    inner class. Very similar to :func:`functools.wraps`.

    .. note::
        This decorator will return a class which seems almost identical to the
        base class, but a ``__wrapped__`` attribute will be added to point to the
        original class. All methods will be wrapped using :func:`functools.wraps`.

    :Example:
        >>> import inspect
        >>>
        >>> class First:
        ...     '''This is the first class.'''
        ...     def __init__(self, a, b):
        ...         pass
        >>>
        >>> @wraps_class(First)
        ... class Second(First):
        ...     '''This is the second class.'''
        ...     def __init__(self, *args, **kwargs):
        ...         super().__init__(*args, **kwargs)
        >>>
        >>> Second.__name__
        'First'
        >>> Second.__doc__
        'This is the first class.'
        >>> str(inspect.signature(Second.__init__))
        '(self, a, b)'
        >>> Second.__wrapped__
        <class 'vanguard.decoratorutils.wrapping.First'>

    :param base_class: The base class to wrap.
    :param decorator_source: If present, any wrapped functions on the class have the attribute
        ``__vanguard_wrap_source__`` set to this value.
    :returns: A function that wraps the class.
    """

    def inner_function(inner_class: type[T]) -> type[T]:
        """Update the values in the inner class."""
        for attribute in WRAPPER_ASSIGNMENTS:
            try:
                base_attribute_value = getattr(base_class, attribute)
            except AttributeError:  # pragma: no cover
                # this should be impossible on Python 3.12; even a completely empty class has all the attributes
                # in `WRAPPER_ASSIGNMENTS`, so we'll never hit an AttributeError here assuming that inner_class is
                # actually a class.
                pass
            else:
                setattr(inner_class, attribute, base_attribute_value)

        for key, value in inner_class.__dict__.items():
            if inspect.isfunction(value):
                try:
                    base_class_method = getattr(base_class, key)
                except AttributeError:
                    continue
                wrapped_method = wraps(base_class_method)(value)
                if decorator_source is not None:
                    wrapped_method.__vanguard_wrap_source__ = decorator_source
                setattr(inner_class, key, wrapped_method)
        inner_class.__wrapped__ = base_class
        if decorator_source is not None:
            inner_class.__vanguard_wrap_source__ = decorator_source
        return inner_class

    return inner_function
