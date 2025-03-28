from __future__ import annotations
from typing import Iterator
import numpy as np
from spatial_inventory_rollback.operating_format.attribute_layer import (
    AttributeLayer,
)
from spatial_inventory_rollback.operating_format.layer import Layer
from spatial_inventory_rollback.raster.raster_bound import RasterBound


class CondensedNLayerStack:
    def __init__(
        self,
        stack_bounds: RasterBound,
        flattened: bool = True,
        nodata: int = -1,
    ):
        self.layers: list[AttributeLayer] = []
        self.stack_bounds = stack_bounds
        self.flattened = flattened
        self.nodata = nodata

    def set_data(self, indices: np.ndarray, data: list[dict]):
        """Assigns data to the stack at the specified raster indices.  The Nth
        row of data will be stored on the Nth layer stored in this class

        Args:
            indices (numpy.ndarray): the array of indices on the stack for
                which to set data.
            data (list): the data to assign to the stack for the
                indices (dictionary of colname: column)
        """
        n_rows = len(next(iter(data.values())))
        cols = list(data.keys())
        if len(self.layers) > 0:
            if cols != self.layers[-1].columns:
                raise AttributeError(
                    f"columns mismatch got '{cols}', expected "
                    f"'{self.layers[-1].columns}'"
                )
        for i in range(n_rows):
            row = tuple([data[col][i] for col in cols])
            if len(self.layers) == i:
                new_layer = AttributeLayer(
                    self.stack_bounds,
                    nodata=self.nodata,
                    columns=cols,
                    unique=True,
                )
                self.layers.append(new_layer)
                new_layer.set_data(indices, row)
            else:
                existing_layer = self.layers[i]
                existing_layer.set_data(indices, row)

    def get_layers(self) -> Iterator[Layer]:
        """Gets the collection of layers stored in this class

        Yields:
            : the sequence of
                layers
        """
        for layer in self.layers:
            yield layer
