from __future__ import annotations
import os
import pandas as pd
import numpy as np
from spatial_inventory_rollback.operating_format.layer import Layer
from spatial_inventory_rollback.operating_format.landscape import Landscape


def get_grouped_areas(layer: Layer, area: np.ndarray) -> pd.DataFrame:
    return (
        pd.DataFrame(
            data={"id": layer.layer_data, "area": area, "pixel_count": 1}
        )
        .groupby("id")
        .sum()
        .reset_index()
    )


def get_inventory_df(inventory_layer: Layer, area: np.ndarray) -> pd.DataFrame:
    df = inventory_layer.select_all()
    df["age"] = df.inventory_year - df.establishment_year
    return df.merge(get_grouped_areas(inventory_layer, area))


def get_disturbance_area_by_type(df: pd.DataFrame, label: str) -> pd.DataFrame:
    df = df[["year", "disturbance_type", "area"]]
    df = df.groupby(["year", "disturbance_type"]).sum().reset_index()
    df = df.pivot(index="year", columns="disturbance_type")
    df.columns = df.columns.droplevel()
    df.columns.name = None
    df.columns = [f"{label} {x} area [ha]" for x in df.columns]
    return df


def get_disturbance_df(
    disturbance_layer: Layer, area: np.ndarray
) -> pd.DataFrame:
    df = disturbance_layer.select_all()
    return df.merge(
        get_grouped_areas(disturbance_layer, area),
        left_on="sequence_id",
        right_on="id",
    ).drop(columns=["id"])


def get_disturbance_comparison(
    pre_rollback_disturbance: pd.DataFrame,
    post_rollback_disturbance: pd.DataFrame,
) -> pd.DataFrame:
    df1 = get_disturbance_area_by_type(
        pre_rollback_disturbance, "pre-rollback"
    )
    df2 = get_disturbance_area_by_type(
        post_rollback_disturbance, "post-rollback"
    )
    result = df1.merge(df2, how="outer", left_index=True, right_index=True)
    return result.fillna(0)


def get_inventory_area_summary(
    pre_rollback_inventory: pd.DataFrame, post_rollback_inventory: pd.DataFrame
) -> pd.DataFrame:
    data = {
        "pre_rollback_raster_area": pre_rollback_inventory.area.sum(),
        "post_rollback_raster_area": post_rollback_inventory.area.sum(),
        "pre_rollback_inventory_area": pre_rollback_inventory[
            pre_rollback_inventory.id > 0
        ].area.sum(),
        "post_rollback_inventory_area": post_rollback_inventory[
            post_rollback_inventory.id > 0
        ].area.sum(),
    }
    inventory_area_summary = pd.DataFrame(index=[1], data=data)
    inventory_area_summary.index.name = "area totals"
    return inventory_area_summary


def get_area_by_age_comparison(
    pre_rollback_inventory: pd.DataFrame, post_rollback_inventory: pd.DataFrame
) -> pd.DataFrame:
    df = pd.DataFrame(
        data={
            "pre_rollback_age": pre_rollback_inventory[["age", "area"]]
            .groupby("age")
            .sum()["area"],
            "post_rollback_age": post_rollback_inventory[["age", "area"]]
            .groupby("age")
            .sum()["area"],
        }
    )
    return df


def get_classifier_area_comparison(
    classifier: str,
    pre_rollback_inventory: pd.DataFrame,
    post_rollback_inventory: pd.DataFrame,
) -> pd.DataFrame:
    return pd.DataFrame(
        data={
            f"pre_rollback_area_by_{classifier}": pre_rollback_inventory[
                [classifier, "area"]
            ]
            .groupby(classifier)
            .sum()["area"],
            f"post_rollback_area_by_{classifier}": post_rollback_inventory[
                [classifier, "area"]
            ]
            .groupby(classifier)
            .sum()["area"],
        }
    )


def get_post_rollback_regen_delays(
    post_rollback_disturbance: pd.DataFrame,
) -> pd.DataFrame:
    regen_delays = post_rollback_disturbance[
        post_rollback_disturbance.regen_delay > 0
    ].copy()
    regen_delays["regen_delay"] = regen_delays["regen_delay"].astype(int)
    return regen_delays[["regen_delay", "area"]].groupby("regen_delay").sum()


def get_rollback_process_summaries(
    area_layer: np.ndarray,
    procedure_info_layer: np.ndarray,
    procedure_info_attributes: pd.DataFrame,
) -> dict[str, pd.DataFrame]:
    area_by_id = (
        pd.DataFrame(data={"id": procedure_info_layer, "area": area_layer})
        .groupby("id")
        .sum()
        .reset_index()
    )
    merged_areas = area_by_id.merge(
        procedure_info_attributes, left_on="id", right_on="id"
    )
    data_columns = [
        col for col in merged_areas.columns if col not in ["id", "area"]
    ]
    output = {}
    for data_col in data_columns:
        output[data_col] = (
            merged_areas[["area", data_col]].groupby(data_col).sum()
        )

    return output


def save_stats_tables(
    output_dir: str,
    pre_rollback_landscape: Landscape,
    post_rollback_landscape: Landscape,
    classifiers: list[str],
    area_layer: np.ndarray,
    procedure_info_layer: np.ndarray,
    procedure_info_attributes: pd.DataFrame,
):
    pre_rollback_disturbance = get_disturbance_df(
        pre_rollback_landscape.get_layer("gcbm_disturbance"), area_layer
    )
    post_rollback_disturbance = get_disturbance_df(
        post_rollback_landscape.get_layer("gcbm_disturbance"), area_layer
    )
    pre_rollback_inventory = get_inventory_df(
        pre_rollback_landscape.get_layer("gcbm_inventory"), area_layer
    )
    post_rollback_inventory = get_inventory_df(
        post_rollback_landscape.get_layer("gcbm_inventory"), area_layer
    )

    def _save(name, df):
        df.to_csv(os.path.join(output_dir, name))

    for name, df in get_rollback_process_summaries(
        area_layer, procedure_info_layer, procedure_info_attributes
    ).items():
        _save(f"{name}.csv", df)

    _save(
        "disturbance_comparison.csv",
        get_disturbance_comparison(
            pre_rollback_disturbance, post_rollback_disturbance
        ),
    )

    _save(
        "inventory_area_summary.csv",
        get_inventory_area_summary(
            pre_rollback_inventory, post_rollback_inventory
        ),
    )

    _save(
        "area_by_age_comparison.csv",
        get_area_by_age_comparison(
            pre_rollback_inventory, post_rollback_inventory
        ),
    )

    for classifier in classifiers:
        _save(
            f"area_by_classifier_{classifier}_comparison.csv",
            get_classifier_area_comparison(
                classifier, pre_rollback_inventory, post_rollback_inventory
            ),
        )

    _save(
        "post_rollback_regen_delays.csv",
        get_post_rollback_regen_delays(post_rollback_disturbance),
    )
