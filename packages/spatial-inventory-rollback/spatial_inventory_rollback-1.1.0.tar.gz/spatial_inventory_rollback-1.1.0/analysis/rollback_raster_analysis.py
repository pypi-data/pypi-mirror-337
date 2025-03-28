import numpy as np
from spatial_inventory_rollback.raster.gdal_helpers import GDALHelperDataset
from spatial_inventory_rollback.raster import wgs84_area
from spatial_inventory_rollback.raster import gdal_helpers


M_2_TO_HA = 0.0001


def compute_area_raster(base_raster_path: str, output_path: str) -> np.ndarray:
    wgs84_area.create_wgs84_area_raster(
        base_raster_path, output_path, M_2_TO_HA
    )
    return gdal_helpers.read_dataset(output_path).data.flatten()


def read_dataset(layer_path: str) -> GDALHelperDataset:
    return gdal_helpers.read_dataset(layer_path)
