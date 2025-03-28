from __future__ import annotations
import sqlite3
import pandas as pd


def load_disturbance_type_order_file(disturbance_type_order_path):
    with open(disturbance_type_order_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    disturbance_type_order = pd.DataFrame({"disturbance_type_name": lines})
    return disturbance_type_order


def load_disturbance_type_order(
    db_path: str, disturbance_type_order_path: str = None
) -> dict[str, int]:
    with sqlite3.connect(db_path) as connection:
        db_dist_types_df = pd.read_sql(
            sql="select name from disturbance_type order by code",
            con=connection,
        )
    dist_type_name_set = None
    disturbance_type_order = None
    if disturbance_type_order_path:
        disturbance_type_order = load_disturbance_type_order_file(
            disturbance_type_order_path
        )

        # do a little validation
        dist_type_name_set = set(
            disturbance_type_order["disturbance_type_name"]
        )
        # check that the names in the file are distinct

        if not len(dist_type_name_set) == len(disturbance_type_order.index):
            raise ValueError(
                f"duplicate values detected in {disturbance_type_order_path}"
            )
        # check that every entry in the file is present in the specified
        # database
        set_diff = dist_type_name_set.difference(
            set(db_dist_types_df["name"].unique())
        )
        if set_diff:
            raise ValueError(
                f"entries in {disturbance_type_order_path} not found "
                f"in database {db_path}: {set_diff}"
            )
    output_order = []
    if disturbance_type_order is not None:
        output_order.extend(
            list(disturbance_type_order["disturbance_type_name"])
        )
        for name in db_dist_types_df["name"]:
            if name not in dist_type_name_set:
                output_order.append(name)
    else:
        output_order.extend(list(db_dist_types_df["name"]))

    return {name: i for i, name in enumerate(output_order)}
