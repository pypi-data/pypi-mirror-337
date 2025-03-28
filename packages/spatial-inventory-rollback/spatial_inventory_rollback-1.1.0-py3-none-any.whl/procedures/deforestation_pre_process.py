import numpy as np
from spatial_inventory_rollback.procedures import work_unit_functions
from spatial_inventory_rollback.operating_format.landscape_work_unit import (
    LandscapeWorkUnit,
)
import enum


class PreprocesResult(enum.Enum):
    NoDeforestation = 0
    PreRollback = 1
    PostRollback = 2
    PreTransitionPeriod = 3


def pre_process(
    work_unit: LandscapeWorkUnit, rollback_year: int
) -> PreprocesResult:
    if not work_unit.facts.deforestation_present:
        return PreprocesResult.NoDeforestation

    inventory = work_unit.layer_data["gcbm_inventory"]
    disturbance = work_unit.layer_data["gcbm_disturbance"]
    # find earliest incidence of deforestation (if any)
    earliest_deforestation_index = work_unit_functions.get_matching_year_index(
        year_array=disturbance["year"],
        year_bound_inclusive=0,
        include_mask=disturbance["is_deforestation"],
        most_recent=False,
    )

    earliest_deforestation_year = disturbance["year"][
        earliest_deforestation_index
    ]

    inventory_delay = rollback_year - earliest_deforestation_year
    if inventory_delay > 20:
        # according to unfccc accounting rules, the deforestation transition
        # period is 20 years. If a deforestation event happened more
        # than 20 years ago, CBM will not need to track the Carbon for
        # that deforested area
        return PreprocesResult.PreTransitionPeriod

    # drop all other events after the earliest deforestation
    work_unit.layer_data[
        "gcbm_disturbance"
    ] = work_unit_functions.filter_events(
        disturbance,
        included=np.logical_or(
            disturbance["year"] < earliest_deforestation_year,
            np.logical_and(
                disturbance["is_deforestation"],
                disturbance["year"] == earliest_deforestation_year,
            ),
        ),
    )

    if inventory_delay > 0:
        inventory["delay"] = inventory_delay
        inventory["establishment_year"] = rollback_year
        return PreprocesResult.PreRollback
    else:
        # indicates a post-rollback deforestation
        inventory["delay"] = 0
        return PreprocesResult.PostRollback
