from __future__ import annotations
import os
from typing import Iterator
import numpy as np
from typing import Union

from spatial_inventory_rollback.raster import gdal_helpers
from spatial_inventory_rollback.raster.raster_bound import RasterBound
from spatial_inventory_rollback.gcbm.gcbm_input import GCBMInput
from spatial_inventory_rollback.gcbm import gcbm_inventory_layer_factory
from spatial_inventory_rollback.gcbm.merge.gcbm_merge_input_db import (
    merge_input_dbs,
)
from spatial_inventory_rollback.gcbm.merge.gcbm_merge_layer_input import (
    MergeInputLayers,
)


def try_extract_float(s: str) -> Union[float, None]:
    try:
        return float(s)
    except ValueError:
        return None


def get_info(
    input_database_path: str,
    study_area_path: str,
    transition_rules_path: str,
    inventory_priority: Union[int, float, str],
) -> dict:
    gcbm_input = GCBMInput(
        input_database_path, study_area_path, transition_rules_path
    )

    inventory_layer_info = (
        gcbm_inventory_layer_factory.get_inventory_layer_info(gcbm_input, None)
    )
    inventory_layer_info["input_database_path"] = input_database_path
    inventory_layer_info["study_area_path"] = study_area_path
    inventory_layer_info["transition_rules_path"] = transition_rules_path
    inventory_layer_info["inventory_priority"] = inventory_priority
    return inventory_layer_info


def yield_layer_info(gcbm_layers: list[MergeInputLayers]) -> Iterator[dict]:
    gcbm_layers_sorted = sorted(
        gcbm_layers, key=lambda x: x.layer_order, reverse=False
    )

    for gcbm_layer in gcbm_layers_sorted:
        yield get_info(
            gcbm_layer.input_database_path,
            gcbm_layer.study_area_path,
            gcbm_layer.transition_rules_path,
            gcbm_layer.inventory_priority,
        )


def yield_disturbance_layer_info(
    gcbm_layers: list[MergeInputLayers],
) -> Iterator[list[dict]]:
    gcbm_layers_sorted = sorted(
        gcbm_layers, key=lambda x: x.layer_order, reverse=False
    )
    for gcbm_layer in gcbm_layers_sorted:
        gcbm_input = GCBMInput(
            gcbm_layer.input_database_path,
            gcbm_layer.study_area_path,
            gcbm_layer.transition_rules_path,
        )
        yield gcbm_input.get_disturbance_layer_info(
            {
                "is_stand_replacing": lambda _: None,
            }
        )


def merge_gcbm_databases(
    gcbm_layers: list[MergeInputLayers], output_dir: str
) -> str:
    input_dbs = [
        layer["input_database_path"] for layer in yield_layer_info(gcbm_layers)
    ]
    output_db = os.path.join(output_dir, "gcbm_input.db")
    merge_input_dbs(input_dbs, output_db)
    return output_db


def get_output_raster_template_path(
    gcbm_layers: list[MergeInputLayers],
) -> str:
    for layer in yield_layer_info(gcbm_layers):
        return layer["establishment"]["path"]


def get_default_layer_source(
    gcbm_layers: list[MergeInputLayers],
) -> MergeInputLayers:
    default_layer_source = None
    for layer in gcbm_layers:
        if layer.default_layer_source:
            if default_layer_source:
                raise ValueError(
                    "exactly one 'default_layer_source' must be specified"
                )

            default_layer_source = layer

    if not default_layer_source:
        raise ValueError(
            "exactly one 'default_layer_source' must be specified"
        )
    return default_layer_source


def get_inventory_priority_fill_value(ascending: bool) -> float:
    if ascending:
        return np.finfo("float").max
    else:
        return np.finfo("float").min


def get_stack_bounds(gcbm_layers: MergeInputLayers) -> RasterBound:
    bounds = None
    for layer in yield_layer_info(gcbm_layers):
        layer_bounds = gdal_helpers.get_raster_dimension(
            layer["establishment"]["path"]
        )
        if bounds is None:
            bounds = layer_bounds
        elif bounds != layer_bounds:
            raise ValueError("bounds mismatch")
    return bounds


def get_output_layer_filename(layer_output_dir: str, name: str) -> str:
    out_dir = os.path.join(layer_output_dir, "merged")
    out_path = os.path.join(out_dir, f"{name}.tiff")
    return out_path


def write_output(
    output_raster_template_path: str,
    output_path: str,
    bound: RasterBound,
    data: np.ndarray,
    nodata: Union[int, float],
) -> None:
    out_dir = os.path.dirname(output_path)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    if not os.path.exists(output_path):
        gdal_helpers.create_empty_raster(
            output_raster_template_path,
            output_path,
            options=gdal_helpers.get_default_geotiff_creation_options(),
            nodata=nodata,
        )
    gdal_helpers.write_output(output_path, data, bound.x_off, bound.y_off)
