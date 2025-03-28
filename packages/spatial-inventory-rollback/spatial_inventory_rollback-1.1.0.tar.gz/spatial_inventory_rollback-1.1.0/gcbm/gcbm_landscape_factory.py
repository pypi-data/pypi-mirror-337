from __future__ import annotations
import os
from spatial_inventory_rollback.application import log_helper
from spatial_inventory_rollback.gcbm.gcbm_input import GCBMInput
from spatial_inventory_rollback.gcbm.rolled_back_gcbm_input import (
    RolledBackGCBMInput,
)
from spatial_inventory_rollback.gcbm import gcbm_disturbance_sequence_factory
from spatial_inventory_rollback.gcbm import gcbm_inventory_layer_factory
from spatial_inventory_rollback.operating_format.landscape import Landscape

logger = log_helper.get_logger()


def create_rolled_back_gcbm_input(
    layer_dir: str, db_path: str, source_gcbm_input: GCBMInput
) -> RolledBackGCBMInput:
    logger.info("load GCBM input")
    study_area_path = os.path.join(layer_dir, "study_area.json")

    gcbm_input = RolledBackGCBMInput(
        source_gcbm_input,
        GCBMInput(
            input_database_path=db_path,
            study_area_path=study_area_path,
            transition_rules_path=os.path.join(
                layer_dir, "transition_rules.csv"
            ),
        ),
    )
    return gcbm_input


def create_gcbm_input(layer_dir: str, db_path: str) -> GCBMInput:
    logger.info("load GCBM input")
    transition_rules_path = os.path.join(layer_dir, "transition_rules.csv")
    if not os.path.exists(transition_rules_path):
        transition_rules_path = None
    study_area_path = os.path.join(layer_dir, "study_area.json")
    gcbm_input = GCBMInput(
        input_database_path=db_path,
        study_area_path=study_area_path,
        transition_rules_path=transition_rules_path,
    )
    return gcbm_input


def create_landscape(
    gcbm_input: GCBMInput,
    inventory_year: int,
    stand_replacing_lookup: dict[str, bool] = None,
    disturbance_type_order: dict[str, int] = None,
) -> Landscape:
    logger.info("reading gcbm inventory")
    gcbm_inventory = gcbm_inventory_layer_factory.assemble_inventory_layer(
        gcbm_input, inventory_year=inventory_year, layer_name="gcbm_inventory"
    )

    logger.info("reading gcbm disturbances")
    gcbm_disturbance = (
        gcbm_disturbance_sequence_factory.assemble_disturbance_sequence_layer(
            gcbm_input,
            layer_name="gcbm_disturbance",
            stand_replacing_lookup=stand_replacing_lookup,
            disturbance_type_order=disturbance_type_order,
        )
    )

    logger.info("assemble landscape")
    landscape = Landscape(gcbm_inventory, gcbm_disturbance)

    return landscape
