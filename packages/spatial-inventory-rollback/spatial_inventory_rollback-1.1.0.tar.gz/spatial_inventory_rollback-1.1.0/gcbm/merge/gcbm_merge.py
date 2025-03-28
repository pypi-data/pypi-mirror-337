from __future__ import annotations
import numpy as np
from spatial_inventory_rollback.raster import raster_chunks
from spatial_inventory_rollback.gcbm.merge import gcbm_merge_methods
from spatial_inventory_rollback.gcbm.merge import gcbm_merge_index
from spatial_inventory_rollback.gcbm.merge import gcbm_merge_inventory
from spatial_inventory_rollback.gcbm.merge import gcbm_merge_disturbance
from spatial_inventory_rollback.gcbm.merge.gcbm_merge_layer_input import (
    MergeInputLayers,
)
from spatial_inventory_rollback.gcbm.merge.gcbm_merge_layer_output import (
    MergeOutputLayers,
)


def merge(
    gcbm_layers: list[MergeInputLayers],
    layer_output_dir: str,
    db_output_dir: str,
    base_simulation_year: int,
    inventory_priority_ascending=True,
    memory_limit_MB=10000,
) -> MergeOutputLayers:
    """Accepts a list of gcbm_layer description objects and creates a merged
    output of age layers, classifier layers and the gcbm input database.

    The merge process selects the age value/classifier from the provided
    spatial layers value which:

        * is defined
        * has the lowest inventory priority value when compared to all other
          passed gcbm_layers. If inventory_priority_ascending=False, then the
          highest inventory priority value is used.
        * in the case of the same inventory priority pixel value the lower
          layer order is used.

    All spatial layers passed to this function will require identical raster
    extent and projection, and if any differences are detected an error will
    be raised.

    The inventory_priority field in the provided object may be a mix of scalar
    float or integer, or a paths to spatial layers whose value is float or
    integer.

    Exactly one layer must specify "default_layer_source=True" and this layer
    will be used as the source for non-age, non-classifier, non-disturbance
    layers in the merged result.  For example the mean_annual_temperature from
    the layer with default_layer_source=True will be passed through to the
    merged output.

    Example::

        merge(
            gcbm_layers=[
                MergeInputLayers(
                    layer_order=1,
                    input_database_path="input1/gcbm_input.db",
                    study_area_path="input1/study_area.json",
                    transition_rules_path="input1/transition_rules.csv",
                    inventory_priority=2021,
                    default_layer_source=True
                ),
                MergeInput(
                    layer_order=2,
                    input_database_path="input2/gcbm_input.db",
                    study_area_path="input2/study_area.json",
                    transition_rules_path="input2/transition_rules.csv",
                    inventory_priority="input2/inventory_year.tiff",
                )
            ]
        )

    Args:
        gcbm_layers (list): list of object describing the order of processing,
            paths and inventory priority for layers to be merged (see example)
        layer_output_dir (str): directory into which merged spatial layers
            will be written
        db_output_dir (str): directory into which the merged gcbm_input db will
            be written.  If the specified dir contains a file named
            "gcbm_input.db" it will be overwritten.
        base_simulation_year (int): the cutoff year for simulation-period
            disturbances, all disturbances prior to this year will be
            considered historic and are used only to inform the GCBM spinup
            procedure.
        inventory_priority_ascending (bool): sets the sort direction for the
            inventory priority
        memory_limit_MB (int, optional): sets the memory limit for spatial
            layer processes.

    Returns:
        MergeOutput: a class describing the paths
            and details for the merge layers process

    """

    # call this for early validation
    gcbm_merge_methods.get_default_layer_source(gcbm_layers)

    stack_bounds = gcbm_merge_methods.get_stack_bounds(gcbm_layers)
    gcbm_layers = list(gcbm_layers)

    output_db_path = gcbm_merge_methods.merge_gcbm_databases(
        gcbm_layers, db_output_dir
    )
    output_raster_template_path = (
        gcbm_merge_methods.get_output_raster_template_path(gcbm_layers)
    )

    chunk_bounds = list(
        raster_chunks.get_memory_limited_raster_chunks(
            n_rasters=4,
            width=stack_bounds.x_size,
            height=stack_bounds.y_size,
            memory_limit_MB=memory_limit_MB,
            bytes_per_pixel=4,
        )
    )
    merged_index_layer_filename = gcbm_merge_methods.get_output_layer_filename(
        layer_output_dir, "merged_index"
    )
    gt_zero_delays_present = False
    for bound in chunk_bounds:
        (
            merge_index,
            inventory_priority,
        ) = gcbm_merge_index.create_spatial_merge_data(
            gcbm_layers, bound, inventory_priority_ascending
        )
        merged_establishment_data = (
            gcbm_merge_inventory.merge_establishment_year(
                gcbm_layers, merge_index, bound
            )
        )

        merged_inventory_delay_data = (
            gcbm_merge_inventory.merge_inventory_delay(
                gcbm_layers, merge_index, bound
            )
        )
        if not gt_zero_delays_present:
            if (merged_inventory_delay_data > 0).any():
                gt_zero_delays_present = True

        gcbm_merge_methods.write_output(
            output_raster_template_path,
            merged_index_layer_filename,
            bound,
            merge_index,
            nodata=-1,
        )
        gcbm_merge_methods.write_output(
            output_raster_template_path,
            gcbm_merge_methods.get_output_layer_filename(
                layer_output_dir, "merged_inventory_priority"
            ),
            bound,
            inventory_priority,
            nodata=gcbm_merge_methods.get_inventory_priority_fill_value(
                inventory_priority_ascending
            ),
        )
        gcbm_merge_methods.write_output(
            output_raster_template_path,
            gcbm_merge_methods.get_output_layer_filename(
                layer_output_dir, "initial_age"
            ),
            bound,
            merged_establishment_data,
            np.iinfo(np.int16).min,
        )

        gcbm_merge_methods.write_output(
            output_raster_template_path,
            gcbm_merge_methods.get_output_layer_filename(
                layer_output_dir, "inventory_delay"
            ),
            bound,
            merged_inventory_delay_data,
            0,
        )

    merged_classifiers = gcbm_merge_inventory.merge_classifiers(
        output_raster_template_path,
        layer_output_dir,
        gcbm_layers,
        merged_index_layer_filename,
        stack_bounds,
        memory_limit_MB,
    )

    merged_disturbances = gcbm_merge_disturbance.merge_disturbances(
        output_raster_template_path,
        layer_output_dir,
        gcbm_layers,
        merged_index_layer_filename,
        merged_classifier_names=list(merged_classifiers.keys()),
        stack_bounds=stack_bounds,
        rollback_year=base_simulation_year,
        memory_limit_MB=memory_limit_MB,
    )

    merged_priority_path = gcbm_merge_methods.get_output_layer_filename(
        layer_output_dir, "merged_inventory_priority"
    )
    merged_inventory_delay_path = (
        gcbm_merge_methods.get_output_layer_filename(
            layer_output_dir, "inventory_delay"
        )
        if gt_zero_delays_present
        else None
    )
    return MergeOutputLayers(
        merged_db_path=output_db_path,
        merged_index_path=gcbm_merge_methods.get_output_layer_filename(
            layer_output_dir, "merged_index"
        ),
        merged_inventory_priority_path=merged_priority_path,
        merged_age_path=gcbm_merge_methods.get_output_layer_filename(
            layer_output_dir, "initial_age"
        ),
        merged_inventory_delay_path=merged_inventory_delay_path,
        merged_classifiers=merged_classifiers,
        merged_disturbances=merged_disturbances,
    )
