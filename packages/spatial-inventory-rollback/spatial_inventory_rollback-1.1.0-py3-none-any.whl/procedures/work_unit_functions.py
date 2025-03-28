from __future__ import annotations
import sys
import numpy as np
import numba


@numba.njit
def _get_earliest_event_idx(
    year: np.ndarray,
    include_mask: np.ndarray,
    min_year: int,
    first_match: bool,
):
    year_compare = -sys.maxsize
    earliest_event_idx = -1
    for i, yr in np.ndenumerate(year):
        if yr >= min_year and include_mask[i]:
            if first_match:
                is_match = yr < year_compare
            else:
                is_match = yr <= year_compare
            if year_compare == -sys.maxsize or is_match:
                year_compare = yr
                earliest_event_idx = i[0]
    return earliest_event_idx


@numba.njit
def _get_latest_event_idx(
    year: np.ndarray,
    include_mask: np.ndarray,
    max_year: int,
    first_match: bool,
):
    year_compare = sys.maxsize
    latest_event_idx = -1
    for i, yr in np.ndenumerate(year):
        if yr <= max_year and include_mask[i]:
            if first_match:
                is_match = yr > year_compare
            else:
                is_match = yr >= year_compare
            if year_compare == sys.maxsize or is_match:
                year_compare = yr
                latest_event_idx = i[0]
    return latest_event_idx


@numba.njit
def get_matching_year_index(
    year_array: np.ndarray,
    year_bound_inclusive: int,
    include_mask: np.ndarray,
    most_recent: bool = True,
):
    idx = -1
    if most_recent:
        idx = _get_latest_event_idx(
            year_array, include_mask, year_bound_inclusive, first_match=False
        )
    else:
        idx = _get_earliest_event_idx(
            year_array, include_mask, year_bound_inclusive, first_match=True
        )
    return idx


def get_nearest_year_index(
    year_array: np.ndarray,
    year_target: int,
    include_mask: np.ndarray,
    first_match: bool,
):
    difference = sys.maxsize
    idx = -1
    for i, yr in np.ndenumerate(year_array):
        diff_i = abs(year_target - yr)
        if first_match:
            is_match = diff_i < difference
        else:
            is_match = diff_i <= difference
        if is_match and include_mask[i]:
            difference = diff_i
            idx = i
    return idx


def compute_rollback_establishment_year(
    inventory: dict, disturbances: dict[str, np.ndarray], rollback_year: int
) -> int:
    if int(rollback_year - inventory["establishment_year"]) > 0:
        return int(inventory["establishment_year"])
    else:
        max_idx = get_matching_year_index(
            year_array=disturbances["year"],
            year_bound_inclusive=rollback_year - 1,
            include_mask=disturbances["is_stand_replacing"],
            most_recent=True,
        )
        if max_idx == -1:
            return None
        return int(disturbances["year"][max_idx])


def filter_events(disturbance: dict[str, np.ndarray], included: np.ndarray):
    return {col: disturbance[col][included] for col in disturbance.keys()}
