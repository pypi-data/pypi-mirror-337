from __future__ import annotations
import os
import numpy as np
import pandas as pd
from spatial_inventory_rollback.analysis import rollback_raster_analysis
from spatial_inventory_rollback.analysis import rollback_tabular_stats
from spatial_inventory_rollback.operating_format import landscape

STATS_DIR = "rollback_stats"


def get_stats_dir(rollback_dir: str) -> str:
    return os.path.join(rollback_dir, STATS_DIR)


def get_pre_rollback_dir(rollback_dir: str) -> str:
    return os.path.join(get_stats_dir(rollback_dir), "pre_rollback_landscape")


def get_post_rollback_dir(rollback_dir: str) -> str:
    return os.path.join(get_stats_dir(rollback_dir), "post_rollback_landscape")


def get_area_raster_path(rollback_dir: str) -> str:
    return os.path.join(get_stats_dir(rollback_dir), "area.tiff")


def generate_area_layer(
    landscape: landscape.Landscape, rollback_dir: str
) -> np.ndarray:
    layer_template_path = None
    for layer in landscape.layers:
        if layer.path:
            layer_template_path = layer.path

    return rollback_raster_analysis.compute_area_raster(
        base_raster_path=layer_template_path,
        output_path=get_area_raster_path(rollback_dir),
    )


def save_stats(rollback_dir: str, classifiers: list[str]) -> None:
    return rollback_tabular_stats.save_stats_tables(
        output_dir=get_stats_dir(rollback_dir),
        pre_rollback_landscape=landscape.load_landscape(
            get_pre_rollback_dir(rollback_dir)
        ),
        post_rollback_landscape=landscape.load_landscape(
            get_post_rollback_dir(rollback_dir)
        ),
        classifiers=classifiers,
        area_layer=rollback_raster_analysis.read_dataset(
            get_area_raster_path(rollback_dir)
        ).data.flatten(),
        procedure_info_layer=rollback_raster_analysis.read_dataset(
            os.path.join(get_stats_dir(rollback_dir), "procedure_info.tiff")
        ).data.flatten(),
        procedure_info_attributes=pd.read_csv(
            os.path.join(get_stats_dir(rollback_dir), "procedure_info.csv")
        ),
    )
