from __future__ import annotations
import os
from tempfile import TemporaryDirectory

from spatial_inventory_rollback.application import log_helper
from spatial_inventory_rollback.operating_format.landscape import Landscape
from spatial_inventory_rollback.operating_format.rollback_output import (
    RollbackOutput,
)
from spatial_inventory_rollback.operating_format.layer import Layer
import mojadata.config

mojadata.config.PROCESS_POOL_SIZE = 1

from mojadata.passthroughgdaltiler2d import (  # noqa: E402
    PassthroughGdalTiler2D,
)
from mojadata.layer.attribute import Attribute  # noqa: E402
from mojadata.layer.rasterlayer import RasterLayer  # noqa: E402
from mojadata.layer.gcbm.disturbancelayer import DisturbanceLayer  # noqa: E402
from mojadata.layer.gcbm.transitionrule import TransitionRule  # noqa: E402
from mojadata.layer.gcbm.transitionrulemanager import (  # noqa: E402
    SharedTransitionRuleManager,
)

logger = log_helper.get_logger()


def write_output(
    output_path: str,
    base_landscape: Landscape,
    rollback_output: RollbackOutput,
) -> None:
    """Writes the accumulated rollback data to spatial layers and metadata
    files.
    """
    logger.info("writing rollback output")
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    base_disturbances = base_landscape.get_layer("gcbm_disturbance")
    base_disturbance_paths = base_disturbances.disturbance_event.path
    base_disturbance_names = [
        os.path.basename(os.path.splitext(path)[0]).split("_moja")[0]
        for path in base_disturbance_paths
    ]

    exclusions_path = os.path.join(output_path, "exclusions.txt")
    open(exclusions_path, "w").write("\n".join(base_disturbance_names))

    with TemporaryDirectory() as tmp_dir:
        mgr = SharedTransitionRuleManager()
        mgr.start()
        rule_manager = mgr.TransitionRuleManager()

        layers = []

        age_path = os.path.join(tmp_dir, "initial_age.tiff")
        base_landscape.create_layer(
            age_path,
            rollback_output.inventory.age_data,
            nodata=rollback_output.inventory.age_nodata,
        )
        layers.append(RasterLayer(age_path, name="initial_age"))

        inventory_delay_path = os.path.join(tmp_dir, "inventory_delay.tiff")
        base_landscape.create_layer(
            inventory_delay_path,
            rollback_output.inventory.delay_data,
            nodata=rollback_output.inventory.delay_nodata,
        )
        layers.append(
            RasterLayer(inventory_delay_path, name="inventory_delay")
        )

        for i, layer in enumerate(
            rollback_output.disturbance_data.get_layers()
        ):
            layer_path = os.path.join(
                tmp_dir, f"rollback_disturbances_{i}.tiff"
            )

            layers.append(
                _create_disturbance_layer(
                    base_landscape, rule_manager, layer, layer_path
                )
            )

        for i, layer in enumerate(
            rollback_output.last_pass_disturbance_data.get_layers()
        ):
            layer_path = os.path.join(
                tmp_dir, f"rollback_last_pass_disturbances_{i}.tiff"
            )

            layers.append(
                _create_disturbance_layer(
                    base_landscape,
                    rule_manager,
                    layer,
                    layer_path,
                    ["last_pass_disturbance"],
                )
            )

        tiler = PassthroughGdalTiler2D()
        tiler.tile(layers, output_path)
        rule_manager.write_rules(
            os.path.join(output_path, "transition_rules.csv")
        )


def _create_disturbance_layer(
    base_landscape: Landscape,
    rule_manager,
    layer: Layer,
    path: str,
    tags: list[str] = None,
) -> DisturbanceLayer:
    base_landscape.create_layer(path, layer.layer_data)

    layer_attributes = layer.select_all()

    attribute_table = {
        str(row.id): row for _, row in layer_attributes.iterrows()
    }

    inventory = base_landscape.get_layer("gcbm_inventory")

    transition_rule = (
        TransitionRule(
            regen_delay=Attribute("regen_delay"),
            age_after=Attribute("age_after"),
            classifiers={c: "?" for c in inventory.classifier_names},
        )
        if "regen_delay" in layer_attributes.columns
        and "age_after" in layer_attributes.columns
        else None
    )

    return DisturbanceLayer(
        rule_manager,
        RasterLayer(
            path,
            attributes=layer_attributes.columns.array,
            attribute_table=attribute_table,
        ),
        year=Attribute("year"),
        disturbance_type=Attribute("disturbance_type"),
        transition=transition_rule,
        tags=tags,
    )
