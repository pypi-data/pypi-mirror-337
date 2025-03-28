from __future__ import annotations
import numpy as np
from spatial_inventory_rollback.operating_format.landscape_work_unit import (
    LandscapeWorkUnit,
)
from spatial_inventory_rollback.operating_format.rollback_output import (
    RollbackOutput,
)
from spatial_inventory_rollback.procedures.disturbance_type_generator import (
    DisturbanceTypeGenerator,
)


def add_random_events(
    random_age_draws: np.ndarray,
    work_unit: LandscapeWorkUnit,
    rollback_output: RollbackOutput,
    establishment_year: int,
    classifier_value_key: dict,
    disturbance_type_generator: DisturbanceTypeGenerator,
    output_events: dict,
):
    grouped_draws = _group_age_draws(random_age_draws)
    single_draw = random_age_draws.shape[0] == 1
    dist_type_distribution_key = classifier_value_key.copy()
    dist_types_by_year = {}
    for i_group, group in enumerate(grouped_draws):
        output_events_copy = output_events.copy()
        for age_draw in group:
            disturbance_year = establishment_year - age_draw
            if disturbance_year in dist_types_by_year:
                dist_type = dist_types_by_year[disturbance_year]
            else:
                dist_type_distribution_key[
                    "disturbance_year"
                ] = disturbance_year
                dist_type = (
                    disturbance_type_generator.get_random_disturbance_type(
                        dist_type_distribution_key
                    )
                )
            output_events_copy.append_events(
                {
                    "year": disturbance_year,
                    "disturbance_type": dist_type,
                    "is_stand_replacing": True,
                    "age_after": 0,
                }
            )
        rollback_output.set_disturbances(
            (work_unit.indices if single_draw else work_unit.indices[i_group]),
            output_events_copy,
        )


def _group_age_draws(random_age_draws: np.ndarray) -> list[np.ndarray]:
    output = []
    for idx in range(random_age_draws.shape[0]):
        group = []
        output.append(group)
        for age_idx in range(random_age_draws.shape[1]):
            draw_value = random_age_draws[idx, age_idx]
            if np.isnan(draw_value):
                break
            group.append(draw_value)
    return output
