from __future__ import annotations
import os
import shutil
from tempfile import TemporaryDirectory
from spatial_inventory_rollback.operating_format import numpy_optimization
from spatial_inventory_rollback.gcbm.merge import gcbm_merge_methods
from spatial_inventory_rollback.raster import gdal_helpers
from spatial_inventory_rollback.raster.raster_bound import RasterBound
from spatial_inventory_rollback.raster import raster_chunks
from spatial_inventory_rollback.operating_format.disturbance_sequence import (
    DisturbanceSequenceLayer,
)
from spatial_inventory_rollback.operating_format.stacked_disturbance_layer import (  # noqa 503
    AttributeSorter,
)
from spatial_inventory_rollback.operating_format.output_events import (
    OutputEvents,
)
from spatial_inventory_rollback.operating_format.condensed_n_layer_stack import (  # noqa 501
    CondensedNLayerStack,
)
from spatial_inventory_rollback.operating_format import (
    disturbance_sequence_factory,
)
from spatial_inventory_rollback.gcbm.merge.gcbm_merge_layer_input import (
    MergeInputLayers,
)


def merge_disturbances(
    output_raster_template_path: str,
    layer_output_dir: str,
    gcbm_layers: list[MergeInputLayers],
    merge_index_path: str,
    merged_classifier_names: list[str],
    stack_bounds: RasterBound,
    rollback_year: int,
    memory_limit_MB: int,
) -> list[dict]:
    chunk_bounds = list(
        raster_chunks.get_memory_limited_raster_chunks(
            n_rasters=2,
            width=stack_bounds.x_size,
            height=stack_bounds.y_size,
            memory_limit_MB=memory_limit_MB,
            bytes_per_pixel=4,
        )
    )
    with TemporaryDirectory() as tempdir:
        disturbance_layer_info = []

        for idx, item in enumerate(
            gcbm_merge_methods.yield_disturbance_layer_info(gcbm_layers)
        ):
            os.makedirs(os.path.join(tempdir, str(idx)))
            for layer_info in item:
                # make a temp copy of the raster, and the attribute table
                copy_path = shutil.copy(
                    src=layer_info["path"], dst=os.path.join(tempdir, str(idx))
                )
                # append a record to the disturbance_layer_info, referencing
                # the temp copy
                disturbance_layer_info.append(
                    {
                        "layer_index": idx,
                        "path": copy_path,
                        "nodata": layer_info["nodata"],
                        "attributes": layer_info["attributes"],
                    }
                )

        for chunk in chunk_bounds:
            # read the merge index
            merge_index_ds = gdal_helpers.read_dataset(merge_index_path, chunk)
            for layer_info in disturbance_layer_info:
                # read the temp copy data
                disturbance_layer_ds = gdal_helpers.read_dataset(
                    layer_info["path"], chunk
                )

                # mask out the pixels based on the merge index in the temp copy
                mask = merge_index_ds.data == layer_info["layer_index"]
                disturbance_layer_ds.data[
                    ~mask | (merge_index_ds.data == merge_index_ds.nodata)
                ] = disturbance_layer_ds.nodata

                # write the masked array back to the temp copy
                gdal_helpers.write_output(
                    layer_info["path"],
                    disturbance_layer_ds.data,
                    chunk.x_off,
                    chunk.y_off,
                )

        if not disturbance_layer_info:
            return []

        output = create_merged_output_layers(
            output_raster_template_path,
            layer_output_dir,
            merged_classifier_names,
            stack_bounds,
            rollback_year,
            disturbance_layer_info,
        )
    return output


def create_merged_output_layers(
    output_raster_template_path,
    layer_output_dir,
    merged_classifier_names,
    stack_bounds,
    rollback_year,
    disturbance_layer_info,
) -> list[dict]:
    output = []
    # this might take a while:
    gcbm_disturbance: DisturbanceSequenceLayer = (
        disturbance_sequence_factory.assemble_disturbance_sequence_layer(
            name="gcbm_disturbance",
            disturbance_layer_info=disturbance_layer_info,
            attribute_sorters=[
                AttributeSorter(
                    "year", lambda year: int(year)
                )  # sort by year asc
            ],
        )
    )
    gcbm_disturbance.flatten()
    sequence_ids = (
        gcbm_disturbance.disturbance_sequence.index.drop_duplicates()
    )
    disturbance_data = CondensedNLayerStack(stack_bounds, flattened=True)
    last_pass_disturbance_data = CondensedNLayerStack(
        stack_bounds, flattened=True
    )
    indexed_where = numpy_optimization.IndexedWhere(
        gcbm_disturbance.layer_data
    )
    for seq_id in sequence_ids:
        output_events = OutputEvents(merged_classifier_names, rollback_year)
        disturbance_events = gcbm_disturbance.select_data(seq_id)
        output_events.append_events(disturbance_events)
        indices = indexed_where.where(seq_id)
        disturbance_data.set_data(indices, output_events.contemporary_data)
        last_pass_disturbance_data.set_data(
            indices, output_events.last_pass_data
        )

    for i, layer in enumerate(disturbance_data.get_layers()):
        layer_path = os.path.join(
            layer_output_dir, f"merged_disturbances_{i}.tiff"
        )
        attributes_path = os.path.join(
            layer_output_dir, f"merged_disturbances_{i}.csv"
        )
        layer.select_all().to_csv(attributes_path, index=False)
        gcbm_merge_methods.write_output(
            output_raster_template_path,
            layer_path,
            stack_bounds,
            layer.layer_data.reshape(
                (stack_bounds.y_size, stack_bounds.x_size)
            ),
            -1,
        )
        output.append(
            {
                "layer_path": layer_path,
                "attribute_path": attributes_path,
                "tags": None,
            }
        )
    for i, layer in enumerate(last_pass_disturbance_data.get_layers()):
        layer_path = os.path.join(
            layer_output_dir, f"merged_last_pass_disturbances_{i}.tiff"
        )
        attributes_path = os.path.join(
            layer_output_dir, f"merged_last_pass_disturbances_{i}.csv"
        )
        layer.select_all().to_csv(attributes_path, index=False)
        gcbm_merge_methods.write_output(
            output_raster_template_path,
            layer_path,
            stack_bounds,
            layer.layer_data.reshape(
                (stack_bounds.y_size, stack_bounds.x_size)
            ),
            -1,
        )
        output.append(
            {
                "layer_path": layer_path,
                "attribute_path": attributes_path,
                "tags": ["last_pass_disturbance"],
            }
        )

    return output
