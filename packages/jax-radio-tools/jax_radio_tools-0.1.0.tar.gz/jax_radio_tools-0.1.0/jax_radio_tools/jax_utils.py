"""
Utility modules required for JAX implementation.

# Copyright(C) 2022 Gordian Edenhofer
# SPDX-License-Identifier: GPL-2.0+ OR BSD-2-Clause
# Authors: Gordian Edenhofer, Philipp Frank
"""

import operator
from abc import ABCMeta
from dataclasses import dataclass
from functools import partial
from typing_extensions import Union

import jax
from jax.tree_util import register_pytree_node, register_pytree_node_class, tree_map
from . import units

"""
Below code is used to define the metaclass that is used for all subsequent definitions
of classes used in this module. It properly takes care of extending PyTree definitions
to 

Obtained from ift/NIFTy/src/re/model.py

# SPDX-License-Identifier: GPL-2.0+ OR BSD-2-Clause 
"""


class ModelMeta(ABCMeta):
    """Register all derived classes as PyTrees in JAX using metaprogramming.

    For any dataclasses.Field property with a metadata-entry named "static",
    we will either hide or expose the property to JAX depending on the value.
    """

    def __new__(mcs, name, bases, dict_, /, **kwargs):
        cls = super().__new__(mcs, name, bases, dict_, **kwargs)
        cls = dataclass(init=False, repr=False, eq=False)(cls)
        IS_STATIC_DEFAULT = True

        def tree_flatten(self):
            static = []
            dynamic = []
            for k, v in self.__dict__.items():
                # Inspired by how equinox registers properties as static in JAX
                fm = self.__dataclass_fields__.get(k)
                fm = fm.metadata if fm is not None else {}
                if fm.get("static", IS_STATIC_DEFAULT) is False:
                    dynamic.append((PyTreeString(k), v))
                else:
                    static.append((k, v))
            return (tuple(dynamic), tuple(static))

        @partial(partial, cls=cls)
        def tree_unflatten(aux, children, *, cls):
            static, dynamic = aux, children
            obj = object.__new__(cls)
            for nm, m in dynamic + static:
                setattr(obj, str(nm), m)  # unwrap any potential `PyTreeSring`s
            return obj

        # Register class and all classes deriving from it
        register_pytree_node(cls, tree_flatten, tree_unflatten)
        return cls


"""
Below code is used to defined PyTreeString objects, which defines strings
as PyTree objects that can be propagated as a dynamic object in the PyTree
structure.

Obtained from ift/NIFTy/src/re/tree_math/pytree_string.py

# SPDX-License-Identifier: GPL-2.0+ OR BSD-2-Clause 
"""


def _unary_op(op, name=None):
    def unary_call(lhs):
        return op(lhs._str)

    name = op.__name__ if name is None else name
    unary_call.__name__ = f"__{name}__"
    return unary_call


def _binary_op(op, name=None):
    def binary_call(lhs, rhs):
        lhs = lhs._str if isinstance(lhs, PyTreeString) else lhs
        rhs = rhs._str if isinstance(rhs, PyTreeString) else rhs
        out = op(lhs, rhs)
        return PyTreeString(out) if isinstance(out, str) else out

    name = op.__name__ if name is None else name
    binary_call.__name__ = f"__{name}__"
    return binary_call


def _rev_binary_op(op, name=None):
    def binary_call(lhs, rhs):
        lhs = lhs._str if isinstance(lhs, PyTreeString) else lhs
        rhs = rhs._str if isinstance(rhs, PyTreeString) else rhs
        out = op(rhs, lhs)
        return PyTreeString(out) if isinstance(out, str) else out

    name = op.__name__ if name is None else name
    binary_call.__name__ = f"__r{name}__"
    return binary_call


def _fwd_rev_binary_op(op, name=None):
    return (_binary_op(op, name=name), _rev_binary_op(op, name=name))


@register_pytree_node_class
class PyTreeString:
    def __init__(self, str):
        self._str = str

    def tree_flatten(self):
        return ((), (self._str,))

    @classmethod
    def tree_unflatten(cls, aux, _):
        return cls(*aux)

    def __str__(self):
        return self._str

    def __repr__(self):
        return f"{self.__class__.__name__}({self._str!r})"

    __lt__ = _binary_op(operator.lt)
    __le__ = _binary_op(operator.le)
    __eq__ = _binary_op(operator.eq)
    __ne__ = _binary_op(operator.ne)
    __ge__ = _binary_op(operator.ge)
    __gt__ = _binary_op(operator.gt)

    __add__, __radd__ = _fwd_rev_binary_op(operator.add)
    __mul__, __rmul__ = _fwd_rev_binary_op(operator.mul)

    lower = _unary_op(str.lower)
    upper = _unary_op(str.upper)

    __hash__ = _unary_op(str.__hash__)

    startswith = _binary_op(str.startswith)


def hide_strings(a):
    return tree_map(lambda x: PyTreeString(x) if isinstance(x, str) else x, a)


def jax_zip(x: jax.typing.ArrayLike, y: jax.typing.ArrayLike) -> list[tuple]:
    """equivalent of zip function in Python"""

    assert x.shape[0] == y.shape[0], "lengths do not match."

    return tree_map(
        lambda xx, yy: jax.numpy.array([[xx[i], yy[i]] for i in range(x.shape[0])]),
        x,
        y,
    )


def jit_repeat(
    a: jax.typing.ArrayLike,
    repeats: jax.typing.ArrayLike,
    axis: Union[int, None],
    total_repeat_length: Union[int, None],
):
    """Jit-compiled version of jax.numpy.repeat."""
    return jax.jit(jax.numpy.repeat, static_argnames=["axis", "total_repeat_length"])(
        a, repeats, axis, total_repeat_length
    )


def resample(
    trace: jax.typing.ArrayLike,
    dt_resample: float = 2 * units.ns,
    dt_sample: float = 0.1 * units.ns,
    times: Union[jax.typing.ArrayLike, None] = None,
    sample_axis: int = 0,
) -> jax.Array:
    """
    Resample the trace to the given sampling frequency.

    This is jaxified from scipy.signal.resample, combined with the
    wrapper call from NuRadioReco.
    We also remove the functionality for complex signals since only
    real signal are applicable in our scenario.

    Parameter:
    ----------
    trace : jax.typing.ArrayLike
        the trace to downsample
    dt_resample : float, default=2 ns
        the time resolution to downsample to.
        Default is 2 ns, which is slightly better than the LOFAR resolution
    dt_sample : float, default=0.1 ns
        the original time resolution. Required for calculating the
        decimation factor
    times : Union[jax.typing.ArrayLike, None], default=None
        the times describing the trace. If provided, the
        new times for the downsampled traces will be returned.
    sample_axis : int, default=0
        the axis where the trace is to downsample

    Return:
    ------
    y : jax.Array
        the downsampled signal
    new_t : jax.Array
        the new time array for the downsampled signal
    """
    trace = jax.numpy.asarray(trace)
    n_samples = trace.shape[sample_axis]
    resampling_factor = dt_resample / dt_sample
    n_resamples = int(n_samples / resampling_factor)  # divide
    trace_fft = jax.numpy.fft.rfft(trace, axis=sample_axis)

    # print(f"Downsampling from {dt_sample:.2f} ns to {dt_resample :.2f} ns")
    # print(f"Corresponding to reduction of {n_samples:d} to {n_resamples:d} number of samples.")

    # Placeholder array for output spectrum
    newshape = list(trace_fft.shape)
    newshape[sample_axis] = n_resamples // 2 + 1
    Y = jax.numpy.zeros(newshape, trace_fft.dtype)

    # Copy positive frequency components (and Nyquist, if present)
    N = min(n_resamples, n_samples)
    nyq = N // 2 + 1  # Slice index that includes Nyquist if present
    sl = [slice(None)] * trace.ndim
    sl[sample_axis] = slice(0, nyq)
    Y = Y.at[tuple(sl)].set(trace_fft[tuple(sl)])

    # Split/join Nyquist component(s) if present
    # So far we have set Y[+N/2]=X[+N/2]
    if N % 2 == 0:
        if n_resamples < n_samples:  # downsampling
            sl[sample_axis] = slice(N // 2, N // 2 + 1)
            Y = Y.at[tuple(sl)].set(Y[tuple(sl)] * 2.0)
        elif n_samples < n_resamples:  # upsampling
            # select the component at frequency +N/2 and halve it
            sl[sample_axis] = slice(N // 2, N // 2 + 1)
            Y = Y.at[tuple(sl)].set(Y[tuple(sl)] * 0.5)

    # Inverse transform
    y = jax.numpy.fft.irfft(Y, n_resamples, axis=sample_axis)
    y *= float(n_resamples) / float(n_samples)

    if times is None:
        return y
    else:
        new_t = (
            jax.numpy.arange(0, n_resamples)
            * (times[1] - times[0])
            * n_samples
            / float(n_resamples)
            + times[0]
        )
        return y, new_t