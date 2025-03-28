from __future__ import annotations
from spatial_inventory_rollback.application import log_helper
import numpy as np
from scipy.sparse import csr_matrix
from numba import njit
from numba.typed import Dict
from numba import types

logger = log_helper.get_logger()


def unique(**kwargs):
    use_unique_view = (
        ("axis" in kwargs and kwargs["axis"] == 0)
        and ("return_inverse" in kwargs and kwargs["return_inverse"])
        and (len(kwargs["ar"].shape) == 2)
    )
    if use_unique_view:
        logger.debug(f"_unique_view {kwargs['ar'].shape}")
        return _unique_view(kwargs["ar"])
    else:
        logger.debug(f"np.unique {kwargs['ar'].shape}")
        return np.unique(**kwargs)


def _unique_view(data: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    b = np.ascontiguousarray(data).view(
        np.dtype((np.void, data.dtype.itemsize * data.shape[1]))
    )
    _, idx, inv = np.unique(b, return_index=True, return_inverse=True)
    return data[idx], inv


class IndexedWhere:
    # see answer here:
    # https://stackoverflow.com/questions/33281957/faster-alternative-to-numpy-where
    def __init__(self, data: np.ndarray):
        # data must be "np.ravel" (ie flattened for this to work correctly)
        if np.ndim(data) > 1:
            raise ValueError("specified array has multiple dimensions")
        self.data = data
        self.index = self.__build_index(data)

    def __build_index(self, data: np.ndarray):
        cols = np.arange(data.size)
        return csr_matrix(
            arg1=(cols, (data, cols)), shape=(data.max() + 1, data.size)
        )

    def where(self, value) -> np.ndarray:
        return self.index[value].data


def map(a: np.ndarray, m: dict) -> np.ndarray:
    """Return the mapped value of a according to the dictionary m.
    Any values in a not present as a key in m will be unchanged.

    The key and values of the dictionary m must be both of the same
    type as the array dtype, and the returned array will be the same
    type as the input array.

    Args:
        a (numpy.ndarray): a numpy array
        m (dict): a dictionary to map values in the resulting array

    Returns:
        numpy.ndarray: the numpy array with replaced mapped values
    """
    dict_type = types.__dict__[str(a.dtype)]
    d = Dict.empty(key_type=dict_type, value_type=dict_type)
    for k, v in m.items():
        d[k] = v
    return _map(a, d)


@njit
def _map(a, m):
    out = a.copy()
    for index, value in np.ndenumerate(a):
        if value in m:
            out[index] = m[value]
    return out
