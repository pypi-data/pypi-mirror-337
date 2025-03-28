from __future__ import annotations
import numpy as np
from spatial_inventory_rollback.raster import gdal_helpers
from spatial_inventory_rollback.raster.raster_bound import RasterBound
from spatial_inventory_rollback.gcbm.merge import gcbm_merge_methods
from spatial_inventory_rollback.gcbm.merge.gcbm_merge_layer_input import (
    MergeInputLayers,
)


def create_spatial_merge_data(
    gcbm_layers: list[MergeInputLayers],
    bounds: RasterBound,
    inventory_priority_ascending=True,
) -> tuple[np.ndarray, np.ndarray]:
    """Creates spatial outputs:

    * merge_index - a layer whose value is the index of the gcbm_layer
      within gcbm_layers.
    * inventory_priority - a layer with the inventory priority value used
      in the resulting merged layer

    Args:
        gcbm_layers (list): list of gcbm input layers
        bounds (RasterBound): stack bounds

    Returns:
        Tuple:
            0: the merge index
            1: the merged inventory priority layer
    """

    merge_index = np.full(
        shape=(bounds.y_size, bounds.x_size), fill_value=-1, dtype=int
    )

    out_inventory_priority = np.full(
        shape=(bounds.y_size, bounds.x_size),
        fill_value=gcbm_merge_methods.get_inventory_priority_fill_value(
            inventory_priority_ascending
        ),
        dtype=float,
    )
    for i_layer, layer in enumerate(
        gcbm_merge_methods.yield_layer_info(gcbm_layers)
    ):
        establishment = gdal_helpers.read_dataset(
            layer["establishment"]["path"], bounds
        )
        inventory_priority_data = None
        float_priority = gcbm_merge_methods.try_extract_float(
            layer["inventory_priority"]
        )
        if float_priority:
            inventory_priority_data = float_priority
        else:
            inventory_priority_data = gdal_helpers.read_dataset(
                layer["inventory_priority"], bounds
            ).data

        priority = (
            inventory_priority_data < out_inventory_priority
            if inventory_priority_ascending
            else inventory_priority_data > out_inventory_priority
        )
        loc = (establishment.data != establishment.nodata) & (priority)
        merge_index[loc] = i_layer
        out_inventory_priority[loc] = (
            inventory_priority_data
            if float_priority
            else inventory_priority_data[loc]
        )
    return merge_index, out_inventory_priority
