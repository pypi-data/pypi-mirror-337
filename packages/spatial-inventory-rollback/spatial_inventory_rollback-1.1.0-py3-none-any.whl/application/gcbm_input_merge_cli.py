from __future__ import annotations

import os
import json
from spatial_inventory_rollback.gcbm.merge import gcbm_merge
from spatial_inventory_rollback.gcbm.merge import gcbm_merge_tile
from spatial_inventory_rollback.gcbm.merge.gcbm_merge_input_db import (
    replace_direct_attached_transition_rules,
)
from argparse import ArgumentParser
from spatial_inventory_rollback.application import log_helper
from spatial_inventory_rollback.gcbm.merge.gcbm_merge_layer_input import (
    MergeInputLayers,
)


def _extract_config(
    layer_dict: dict[str, str], base_dir: str
) -> MergeInputLayers:
    _layer_dict = layer_dict.copy()
    for k, v in _layer_dict.items():
        if k.endswith("_path") and v:
            if not os.path.isabs(v):
                _layer_dict[k] = os.path.relpath(v, base_dir)
                if not os.path.exists(_layer_dict[k]):
                    raise ValueError(
                        f"specified path {_layer_dict[k]} does not exist"
                    )
        elif k == "inventory_priority":
            # inventory priority may be either a int/float or a path
            if not gcbm_merge._try_extract_float(v):
                _layer_dict[k] = os.path.relpath(v, base_dir)
                if not os.path.exists(_layer_dict[k]):
                    raise ValueError(
                        f"specified path {_layer_dict[k]} does not exist"
                    )
    return MergeInputLayers(**_layer_dict)


def cli():
    parser = ArgumentParser(
        description="Merge 2 or more spatially aligned GCBM inputs"
    )
    parser.add_argument(
        "--input_layer_description",
        help="path to json formatted config file",
        type=os.path.abspath,
        required=True,
    )

    parser.add_argument(
        "--layer_output_dir",
        help="output dir for merged layers",
        type=os.path.abspath,
        required=True,
    )

    parser.add_argument(
        "--db_output_dir",
        help="output path for merged GCBM input database",
        type=os.path.abspath,
        required=True,
    )

    parser.add_argument(
        "--memory_limit_MB",
        help=(
            "The upper limit for memory storage during processing of raster "
            "layers. If unspecified 10000 is used"
        ),
        type=int,
        required=False,
    )
    parser.add_argument(
        "--base_simulation_year",
        help=(
            "The cutoff year for simulation-period disturbances, all "
            "disturbances prior to this year will be considered historic "
            "and are used only to inform the GCBM spinup procedure."
            "Defaults to 1990."
        ),
        type=int,
        required=False,
    )
    parser.add_argument(
        "--inventory_priority_ascending",
        help=(
            "Boolean value that sets the sort direction for inventory "
            "priority. If True pixels with the lowest inventory priority "
            "value will be favoured in the merged output, and if False the "
            "highest value is favoured.  Defaults to True."
        ),
        required=False,
    )
    parser.set_defaults(
        memory_limit_MB=10000,
        inventory_priority_ascending=True,
        base_simulation_year=1990,
    )

    args = parser.parse_args()
    log_helper.start_logging("INFO")
    logger = log_helper.get_logger()
    logger.info("start up")

    with open(args.input_layer_description) as config_fp:
        config_list = json.load(config_fp)
    base_dir = os.path.dirname(args.input_layer_description)
    layers = [
        _extract_config(layer_dict, base_dir) for layer_dict in config_list
    ]

    logger.info("merge process start")

    merged_data = gcbm_merge.merge(
        gcbm_layers=layers,
        layer_output_dir=args.layer_output_dir,
        db_output_dir=args.db_output_dir,
        base_simulation_year=args.base_simulation_year,
        inventory_priority_ascending=args.inventory_priority_ascending,
        memory_limit_MB=args.memory_limit_MB,
    )

    gcbm_merge_tile.tile(args.layer_output_dir, merged_data, layers)

    replace_direct_attached_transition_rules(
        os.path.join(args.db_output_dir, "gcbm_input.db"),
        os.path.join(args.layer_output_dir, "transition_rules.csv"),
    )


if __name__ == "__main__":
    cli()
