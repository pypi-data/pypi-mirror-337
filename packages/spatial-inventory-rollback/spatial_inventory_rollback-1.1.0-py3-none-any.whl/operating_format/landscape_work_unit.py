import numpy as np


class LandscapeWorkUnit:
    """A work unit is a group of pixels with a common establishment year
    and disturbance sequence.

    Args:
        indices (numpy.ndarray): the indices on the raster stack that share
            this inventory record and disturbance sequence.
        layer_data (dict): a dictionary of layer.name to layer data for the
            work unit
    """

    def __init__(self, indices: np.ndarray, layer_data: dict):
        self._layer_data = layer_data
        self._indices = indices

    def get_layer(self, layer_name: str):
        return self._layer_data[layer_name]

    @property
    def layer_data(self) -> dict:
        return self._layer_data

    @property
    def indices(self) -> np.ndarray:
        return self._indices
