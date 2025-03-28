from __future__ import annotations
import os
import json
from spatial_inventory_rollback.application.rollback_app_parameters import (
    RollbackAppParameters,
)
from spatial_inventory_rollback.application import log_helper
from spatial_inventory_rollback.gcbm import gcbm_landscape_factory
from spatial_inventory_rollback.procedures import rollback_manager_factory
from spatial_inventory_rollback.analysis import rollback_stats
from spatial_inventory_rollback.gcbm import gcbm_output_writer
from spatial_inventory_rollback.gcbm.gcbm_input import GCBMInput
from spatial_inventory_rollback.analysis import report_writer
from spatial_inventory_rollback.gcbm import gcbm_disturbance_type_order

logger = log_helper.get_logger()


def _rollback(
    gcbm_input: GCBMInput,
    stand_replacing_lookup: dict[str, bool],
    disturbance_type_order: dict[str, int],
    params: RollbackAppParameters,
) -> None:
    landscape = gcbm_landscape_factory.create_landscape(
        gcbm_input=gcbm_input,
        inventory_year=params.inventory_year,
        stand_replacing_lookup=stand_replacing_lookup,
        disturbance_type_order=disturbance_type_order,
    )
    if (
        params.establishment_disturbance_type
        and params.establishment_disturbance_type_distribution
    ):
        raise ValueError(
            "cannot specify both establishment_disturbance_type, and "
            "establishment_disturbance_type_distribution"
        )
    elif params.establishment_disturbance_type:
        disturbance_type_generator_confg = [
            {"distribution": [[params.establishment_disturbance_type, 1.0]]}
        ]
    else:
        disturbance_type_generator_confg = (
            params.establishment_disturbance_type_distribution
        )
    rollback = rollback_manager_factory.get_rollback_manager(
        rollback_year=params.rollback_year,
        age_class_distribution=params.rollback_age_distribution,
        prioritize_disturbances=params.prioritize_disturbances,
        landscape=landscape,
        disturbance_type_generator_config=disturbance_type_generator_confg,
        single_draw=params.single_draw,
        inventory_year=params.inventory_year,
    )
    logger.info("run rollback")

    rollback_output = rollback.rollback(landscape)
    gcbm_output_writer.write_output(
        output_path=params.output_path,
        base_landscape=landscape,
        rollback_output=rollback_output,
    )

    logger.info("save procedure info layer")

    _write_procedure_info(params, landscape, rollback)
    rollback.get_multiple_matching_procedures().to_csv(
        os.path.join(params.output_path, "multiple_matching_procedures.csv"),
        index=False,
    )
    logger.info("save pre-rollback landscape")
    landscape.save(rollback_stats.get_pre_rollback_dir(params.output_path))


def _write_procedure_info(params, landscape, rollback):
    out_dir = rollback_stats.get_stats_dir(params.output_path)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    landscape.create_layer(
        os.path.join(out_dir, "procedure_info.tiff"),
        rollback.procedure_info_layer.layer_data,
        nodata=rollback.procedure_info_layer.nodata,
    )
    rollback.procedure_info_layer.select_all().to_csv(
        os.path.join(out_dir, "procedure_info.csv"), index=False
    )


def _process_rollback_stats(
    gcbm_input: GCBMInput,
    stand_replacing_lookup: dict[str, bool],
    disturbance_type_order: dict[str, int],
    params: RollbackAppParameters,
) -> None:
    logger.info("load rolled back landscape")
    gcbm_input = gcbm_landscape_factory.create_rolled_back_gcbm_input(
        layer_dir=params.output_path,
        db_path=params.input_db,
        source_gcbm_input=gcbm_input,
    )
    rollback_landscape = gcbm_landscape_factory.create_landscape(
        gcbm_input=gcbm_input,
        inventory_year=params.rollback_year,
        stand_replacing_lookup=stand_replacing_lookup,
        disturbance_type_order=disturbance_type_order,
    )
    logger.info("generate area layer")
    rollback_stats.generate_area_layer(rollback_landscape, params.output_path)
    logger.info("save post-rollback landscape")
    rollback_landscape.save(
        rollback_stats.get_post_rollback_dir(params.output_path)
    )
    rollback_stats.save_stats(
        rollback_dir=params.output_path,
        classifiers=[
            x["name"] for x in gcbm_input.get_classifier_layer_info()
        ],
    )
    stats_dir = rollback_stats.get_stats_dir(params.output_path)
    report_writer.generate_report(
        os.path.join(stats_dir, "rollback_report.html"), working_dir=stats_dir
    )


def run(params: RollbackAppParameters) -> None:
    gcbm_input = gcbm_landscape_factory.create_gcbm_input(
        params.input_layers, params.input_db
    )
    stand_replacing_lookup = (
        json.load(open(params.stand_replacing_lookup, encoding="utf-8"))
        if params.stand_replacing_lookup
        else None
    )
    disturbance_type_order = (
        gcbm_disturbance_type_order.load_disturbance_type_order(
            params.input_db, params.disturbance_type_order
        )
    )
    _rollback(
        gcbm_input, stand_replacing_lookup, disturbance_type_order, params
    )
    _process_rollback_stats(
        gcbm_input, stand_replacing_lookup, disturbance_type_order, params
    )
