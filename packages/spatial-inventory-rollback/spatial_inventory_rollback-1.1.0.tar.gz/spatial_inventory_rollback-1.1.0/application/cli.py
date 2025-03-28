import os
import sys
from argparse import ArgumentParser
from spatial_inventory_rollback.application import app
from spatial_inventory_rollback.application import log_helper
from spatial_inventory_rollback.application.rollback_app_parameters import (
    RollbackAppParameters,
)


def _is_integer(n: str) -> bool:
    try:
        float(n)
    except ValueError:
        return False
    else:
        return float(n).is_integer()


def parse_args(args):
    parser = ArgumentParser(
        description="Perform a basic spatial rollback on a GCBM project.",
    )

    parser.add_argument(
        "input_layers",
        help="Path to GCBM tiled layers directory",
        type=os.path.abspath,
    )
    parser.add_argument(
        "input_db", help="Path to GCBM input database", type=os.path.abspath
    )

    parser.add_argument(
        "inventory_year",
        help="Original inventory vintage. Either an integer or a path to an "
        "integer raster layer ",
        type=(lambda x: int(x) if _is_integer(x) else os.path.abspath(x)),
    )
    parser.add_argument(
        "rollback_age_distribution",
        help="Path to rollback age distribution json config file",
        type=os.path.abspath,
    )
    parser.add_argument(
        "--output_path",
        help="Output path",
        type=os.path.abspath,
        required=False,
    )
    parser.add_argument(
        "--rollback_year", help="Rollback year", type=int, required=False
    )
    parser.add_argument(
        "--prioritize_disturbances",
        dest="prioritize_disturbances",
        required=False,
        action="store_true",
    )
    parser.add_argument(
        "--stand_replacing_lookup", required=False, type=os.path.abspath
    )
    parser.add_argument(
        "--disturbance_type_order", required=False, type=os.path.abspath
    )
    parser.add_argument("--logging_level", required=False)
    parser.add_argument("--establishment_disturbance_type", required=False)
    parser.add_argument(
        "--establishment_disturbance_type_distribution", required=False
    )
    parser.add_argument(
        "--single_draw",
        dest="single_draw",
        required=False,
        action="store_true",
    )

    parser.set_defaults(
        output_path=None,
        rollback_year=1990,
        prioritize_disturbances=False,
        logging_level="INFO",
        establishment_disturbance_type=None,
        establishment_disturbance_type_distribution=None,
        single_draw=False,
    )

    parsed_args = parser.parse_args(args)
    return parsed_args


def cli(args):
    log_helper.start_logging(args.logging_level)
    logger = log_helper.get_logger()
    logger.info("start up")
    logger.info(vars(args))

    if not args.output_path:
        args.output_path = os.path.abspath(
            os.path.join(args.input_layers, "..", "rollback")
        )

    try:
        app_params = RollbackAppParameters(**vars(args))
        app.run(app_params)

    except Exception:
        logger.exception("")


if __name__ == "__main__":
    cli(parse_args(sys.argv[1:]))
