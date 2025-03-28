from __future__ import annotations
import numpy as np
from spatial_inventory_rollback.raster.raster_bound import RasterBound
from spatial_inventory_rollback.raster import gdal_helpers
from spatial_inventory_rollback.raster import raster_chunks
from spatial_inventory_rollback.gcbm.merge import gcbm_merge_methods
from spatial_inventory_rollback.gcbm.merge.gcbm_merge_layer_input import (
    MergeInputLayers,
)


def merge_inventory_delay(
    gcbm_layers: list[MergeInputLayers],
    merge_index: np.ndarray,
    bounds: RasterBound,
) -> np.ndarray:
    output_data = np.full(
        shape=(bounds.y_size, bounds.x_size),
        fill_value=0,
        dtype="int16",
    )

    for i_layer, layer in enumerate(
        gcbm_merge_methods.yield_layer_info(gcbm_layers)
    ):
        if "delay" in layer:
            delay_dataset = gdal_helpers.read_dataset(
                layer["delay"]["path"], bounds
            )

            loc = (merge_index == i_layer) & (
                delay_dataset.data != delay_dataset.nodata
            )
            output_data[loc] = delay_dataset.data[loc]
    return output_data


def merge_establishment_year(
    gcbm_layers: list[MergeInputLayers],
    merge_index: np.ndarray,
    bounds: RasterBound,
) -> np.ndarray:
    output_data = np.full(
        shape=(bounds.y_size, bounds.x_size),
        fill_value=np.iinfo(np.int16).min,
        dtype="int16",
    )

    for i_layer, layer in enumerate(
        gcbm_merge_methods.yield_layer_info(gcbm_layers)
    ):
        establishment_dataset = gdal_helpers.read_dataset(
            layer["establishment"]["path"], bounds
        )

        loc = (merge_index == i_layer) & (
            establishment_dataset.data != establishment_dataset.nodata
        )
        output_data[loc] = establishment_dataset.data[loc]
    return output_data


def merge_classifiers(
    output_raster_template_path: str,
    layer_output_dir: str,
    gcbm_layers: list[MergeInputLayers],
    merge_index_path: str,
    stack_bounds: RasterBound,
    memory_limit_MB: int,
) -> dict:
    # create the set of unique classifier names
    merged_classifiers = {}

    inverted_attributes = {}
    distinct_classifiers = set()

    for layer in gcbm_merge_methods.yield_layer_info(gcbm_layers):
        for classifier in layer["classifiers"]:
            distinct_classifiers.add(classifier["name"])

    chunk_bounds = list(
        raster_chunks.get_memory_limited_raster_chunks(
            n_rasters=len(distinct_classifiers) + 1,
            width=stack_bounds.x_size,
            height=stack_bounds.y_size,
            memory_limit_MB=memory_limit_MB,
            bytes_per_pixel=4,
        )
    )
    for bound in chunk_bounds:
        merged_classifiers_data = {}
        for i_layer, layer in enumerate(
            gcbm_merge_methods.yield_layer_info(gcbm_layers)
        ):
            merge_index = gdal_helpers.read_dataset(
                merge_index_path, bound
            ).data
            for classifier in layer["classifiers"]:
                _merge_classifiers_chunk(
                    i_layer,
                    merge_index,
                    classifier,
                    merged_classifiers,
                    inverted_attributes,
                    merged_classifiers_data,
                    bound,
                )

        for classifier_name in merged_classifiers_data.keys():
            gcbm_merge_methods.write_output(
                output_raster_template_path,
                gcbm_merge_methods.get_output_layer_filename(
                    layer_output_dir, classifier_name
                ),
                bound,
                merged_classifiers_data[classifier_name],
                -1,
            )
    for classifier_name in merged_classifiers.keys():
        merged_classifiers[classifier_name][
            "path"
        ] = gcbm_merge_methods.get_output_layer_filename(
            layer_output_dir, classifier_name
        )
    return merged_classifiers


def _merge_classifiers_chunk(
    i_layer: int,
    merge_index: np.ndarray,
    classifier: dict,
    merged_classifiers: dict,
    inverted_attributes: dict,
    merged_classifiers_data: dict,
    bound: RasterBound,
):
    classifier_name = classifier["name"]
    incoming_classifier_data = gdal_helpers.read_dataset(
        classifier["path"], bound
    ).data
    if classifier_name not in merged_classifiers:
        merged_classifiers[classifier_name] = {
            "path": f"{classifier_name}_moja.tiff",
            "name": classifier_name,
            "nodata": -1,
            "attributes": {},
        }
        inverted_attributes[classifier_name] = {}
        merged_classifiers_data[classifier_name] = np.full(
            shape=(bound.y_size, bound.x_size),
            fill_value=-1,
            dtype=int,
        )

    merged_classifier = merged_classifiers[classifier_name]

    out_classifier_data = merged_classifiers_data[classifier_name]

    for att_id, att_name in classifier["attributes"].items():
        att_id = int(att_id)
        if att_id == -1:
            raise ValueError(
                "attribute ids cannot be -1, as this is reserved for the "
                "nodata value"
            )
        output_att_id = None
        if att_name in inverted_attributes[classifier_name]:
            if inverted_attributes[classifier_name][att_name] == att_id:
                output_att_id = (
                    att_id  # no action required, name/id match exactly
                )
            else:
                output_att_id = inverted_attributes[classifier_name][att_name]
        else:
            if att_id in merged_classifier["attributes"]:
                # generate a new att_id, so we dont overwrite an
                # existing one
                output_att_id = len(merged_classifier["attributes"]) + 1
            else:
                output_att_id = att_id
            # add the classifier attribute to the merged layer
            merged_classifier["attributes"][output_att_id] = att_name
            inverted_attributes[classifier_name][att_name] = output_att_id

        loc = (merge_index == i_layer) & (incoming_classifier_data == att_id)
        out_classifier_data[loc] = output_att_id
