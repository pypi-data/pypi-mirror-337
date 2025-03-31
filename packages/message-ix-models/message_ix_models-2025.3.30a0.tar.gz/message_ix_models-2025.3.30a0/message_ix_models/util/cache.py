"""Cache data for expensive operations.

This module extends :class:`genno.caching.Encoder` to handle classes common in
:mod:`message_ix_models`, so these can be used as arguments to cached functions and
included in the computed cache key:

- :class:`sdmx.model.IdentifiableArtefact`, including :class:`.Code`: hashed as their
  string representation / ID.
- :class:`ixmp.Platform`, :class:`xarray.Dataset`: ignored, with a warning logged.
- :class:`.ScenarioInfo`: only the :attr:`~ScenarioInfo.set` entries are hashed.
"""

import json
import logging
from collections.abc import Callable
from dataclasses import is_dataclass
from enum import Enum
from types import FunctionType
from typing import TYPE_CHECKING, Union

import genno.caching
import ixmp
import sdmx.model
import xarray as xr

from message_ix_models.types import AnyQuantity

from ._dataclasses import asdict
from .context import Context
from .scenarioinfo import ScenarioInfo

if TYPE_CHECKING:
    from pathlib import Path


log = logging.getLogger(__name__)


#: Controls whether cached data is returned for functions decorated with
#: :func:`.cached`. Set to :obj:`True` to force reload.
SKIP_CACHE = False

# Paths already logged, to decrease verbosity
PATHS_SEEN: set["Path"] = set()


# Show genno how to hash function arguments seen in message_ix_models


def _quantity(o: "AnyQuantity"):
    return tuple(o.to_series().to_dict())


try:
    genno.caching.Encoder.register(AnyQuantity)(_quantity)
except TypeError:  # Python 3.10 or earlier
    from genno.core.attrseries import AttrSeries
    from genno.core.sparsedataarray import SparseDataArray

    genno.caching.Encoder.register(AttrSeries)(_quantity)
    genno.caching.Encoder.register(SparseDataArray)(_quantity)


# Upstream
@genno.caching.Encoder.register
def _enum(o: Enum):
    return repr(o)


@genno.caching.Encoder.register
def _sdmx_identifiable(o: sdmx.model.IdentifiableArtefact):
    return str(o)


@genno.caching.Encoder.register
def _sdmx_internationalstring(o: sdmx.model.InternationalString):
    return tuple(o.localizations)


# First-party
@genno.caching.Encoder.register
def _context(o: Context):
    return o.asdict()


@genno.caching.Encoder.register
def _dataclass(o: object):
    return (
        asdict(o)
        if (is_dataclass(o) and not isinstance(o, type))
        else json.JSONEncoder().default(o)
    )


@genno.caching.Encoder.register
def _repr_only(o: Union[FunctionType]):
    return repr(o)


@genno.caching.Encoder.register
def _si(o: ScenarioInfo):
    return dict(o.set)


genno.caching.Encoder.ignore(xr.DataArray, xr.Dataset, ixmp.Platform)


def cached(func: Callable) -> Callable:
    """Decorator to cache the return value of a function `func`.

    On a first call, the data requested is returned and also cached under
    :meth:`.Context.get_cache_path`. On subsequent calls, if the cache exists, it is
    used instead of calling the (possibly slow) `func`.

    When :data:`.SKIP_CACHE` is true, `func` is always called.

    See also
    --------
    :doc:`genno:cache` in the :mod:`genno` documentation
    """
    # Determine and create the cache path
    cache_path = Context.get_instance(-1).core.cache_path
    assert cache_path

    if cache_path not in PATHS_SEEN:
        log.debug(f"{func.__name__}() will cache in {cache_path}")
        PATHS_SEEN.add(cache_path)
        cache_path.mkdir(parents=True, exist_ok=True)

    # Use the genno internals to wrap the function.
    cached_load = genno.caching.decorate(
        func, cache_path=cache_path, cache_skip=SKIP_CACHE
    )

    if cached_load.__doc__ is not None:
        # Determine the indent
        line = cached_load.__doc__.split("\n")[-1]
        indent = len(line) - len(line.lstrip(" "))

        # Add a note that the results are cached
        cached_load.__doc__ += (
            f"\n\n{' ' * indent}Data returned by this function is cached using "
            ":func:`.cached`; see also :data:`.SKIP_CACHE`."
        )

    return cached_load
