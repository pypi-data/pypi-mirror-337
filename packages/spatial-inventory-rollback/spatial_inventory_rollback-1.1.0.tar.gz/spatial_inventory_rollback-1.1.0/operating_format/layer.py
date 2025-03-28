import numpy as np
import pandas as pd
from spatial_inventory_rollback.raster.raster_bound import RasterBound


class Layer:
    @property
    def path(self) -> str:
        raise NotImplementedError()

    @property
    def bounds(self) -> RasterBound:
        raise NotImplementedError()

    @property
    def stack_bounds(self) -> RasterBound:
        raise NotImplementedError()

    @property
    def layer_data(self) -> np.ndarray:
        raise NotImplementedError()

    def flatten(self):
        raise NotImplementedError()

    def select_data(self, layer_id: int):
        raise NotImplementedError()

    def select_all(self) -> pd.DataFrame:
        raise NotImplementedError()
