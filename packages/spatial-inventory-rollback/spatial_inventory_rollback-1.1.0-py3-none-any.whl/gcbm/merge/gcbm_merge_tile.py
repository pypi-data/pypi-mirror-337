from __future__ import annotations
import os
import pandas as pd
import mojadata.config
from spatial_inventory_rollback.gcbm.merge import gcbm_merge_methods
from spatial_inventory_rollback.gcbm.gcbm_input import GCBMInput
from spatial_inventory_rollback.gcbm.merge.gcbm_merge_layer_input import (
    MergeInputLayers,
)
from spatial_inventory_rollback.gcbm.merge.gcbm_merge_layer_output import (
    MergeOutputLayers,
)

mojadata.config.PROCESS_POOL_SIZE = 1

from mojadata.passthroughgdaltiler2d import (  # noqa: E402
    PassthroughGdalTiler2D,
)
from mojadata.layer.rasterlayer import RasterLayer  # noqa: E402
from mojadata.layer.gcbm.transitionrulemanager import (  # noqa: E402
    SharedTransitionRuleManager,
)
from mojadata.layer.attribute import Attribute  # noqa: E402
from mojadata.layer.gcbm.disturbancelayer import DisturbanceLayer  # noqa: E402
from mojadata.layer.gcbm.transitionrule import TransitionRule  # noqa: E402


def _get_default_layers(gcbm_layer: MergeInputLayers) -> list[dict]:
    gcbm_input = GCBMInput(
        gcbm_layer.input_database_path,
        gcbm_layer.study_area_path,
        gcbm_layer.transition_rules_path,
    )
    return gcbm_input.get_other_layer_info()


def _create_disturbance_layer(
    classifier_names: list[str],
    rule_manager,
    layer_path: str,
    layer_attribute_csv_path: str,
    tags: list[str] = None,
) -> DisturbanceLayer:
    layer_attributes = pd.read_csv(layer_attribute_csv_path)

    attribute_table = {
        int(row.id): [str(x) for x in row]
        for _, row in layer_attributes.iterrows()
    }

    transition_rule = (
        TransitionRule(
            regen_delay=Attribute("regen_delay"),
            age_after=Attribute("age_after"),
            # TODO classifiers needs checking: list of str or list of
            # Attribute objects
            classifiers=classifier_names,
        )
        if "regen_delay" in layer_attributes.columns
        and "age_after" in layer_attributes.columns
        else None
    )

    return DisturbanceLayer(
        rule_manager,
        RasterLayer(
            layer_path,
            attributes=list(layer_attributes.columns),
            attribute_table=attribute_table,
        ),
        year=Attribute("year"),
        disturbance_type=Attribute("disturbance_type"),
        transition=transition_rule,
        tags=tags,
    )


def tile(
    layer_output_dir: str,
    merged_data: MergeOutputLayers,
    gcbm_layers: list[MergeInputLayers],
    include_index_layer: bool = False,
) -> None:
    mgr = SharedTransitionRuleManager()
    mgr.start()

    rule_manager = mgr.TransitionRuleManager()

    layers = []

    layers.append(RasterLayer(merged_data.merged_age_path, name="initial_age"))
    if merged_data.merged_inventory_delay_path:
        layers.append(
            RasterLayer(
                merged_data.merged_inventory_delay_path, "inventory_delay"
            )
        )
    for (
        classifier_name,
        classifier_info,
    ) in merged_data.merged_classifiers.items():
        layers.append(
            RasterLayer(
                classifier_info["path"],
                name=classifier_name,
                tags=["classifier"],
                attribute_table={
                    int(k): [v]
                    for k, v in classifier_info["attributes"].items()
                },
            )
        )

    for layer_info in _get_default_layers(
        gcbm_merge_methods.get_default_layer_source(gcbm_layers)
    ):
        if "attributes" in layer_info:
            attribute_table = {
                int(k): [v] for k, v in layer_info["attributes"].items()
            }
        else:
            attribute_table = None

        layers.append(
            RasterLayer(
                layer_info["path"],
                name=layer_info["name"],
                tags=[],
                attribute_table=attribute_table,
            )
        )

    for disturbance_info in merged_data.merged_disturbances:
        layers.append(
            _create_disturbance_layer(
                classifier_names=list(merged_data.merged_classifiers.keys()),
                rule_manager=rule_manager,
                layer_path=disturbance_info["layer_path"],
                layer_attribute_csv_path=disturbance_info["attribute_path"],
                tags=disturbance_info["tags"],
            )
        )

    if include_index_layer:
        layers.append(
            RasterLayer(
                merged_data.merged_index_path,
                "merged_index",
                tags=["reporting_classifier"],
            )
        )

    tiler = PassthroughGdalTiler2D()

    tiler.tile(layers, layer_output_dir)

    rule_manager.write_rules(
        os.path.join(layer_output_dir, "transition_rules.csv")
    )
