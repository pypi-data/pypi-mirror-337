from __future__ import annotations
import numpy as np
import pandas as pd
from typing import Union


def null_inventory(inventory) -> bool:
    return bool(pd.isnull(inventory["establishment_year"]))


def rollback_period_sr_disturbances_count(
    disturbances: dict[str, np.ndarray],
    rollback_year: int,
    inventory_year: int,
) -> bool:
    return np.count_nonzero(
        np.logical_and(
            np.logical_and(
                disturbances["year"] >= rollback_year,
                disturbances["year"] <= inventory_year,
            ),
            disturbances["is_stand_replacing"],
        )
    )


def pre_rollback_sr_disturbances(
    disturbances: dict[str, np.ndarray], rollback_year: int
) -> bool:
    return np.logical_and(
        disturbances["year"] < rollback_year,
        disturbances["is_stand_replacing"],
    ).any()


def pre_est_post_rollback_sr_disturbances(
    disturbances: dict[str, np.ndarray],
    rollback_year: int,
    establishment_year: int,
) -> bool:
    return np.logical_and(
        np.logical_and(
            disturbances["year"] >= rollback_year,
            disturbances["year"] <= establishment_year,
        ),
        disturbances["is_stand_replacing"],
    ).any()


def sr_disturbance_after_establishment(
    disturbances: dict[str, np.ndarray],
    establishment_year: int,
    inventory_year: int,
) -> bool:
    return np.logical_and(
        np.logical_and(
            disturbances["year"] > establishment_year,
            disturbances["is_stand_replacing"],
        ),
        disturbances["year"] <= inventory_year,
    ).any()


def establishment_before_rollback(inventory: dict, rollback_year: int) -> bool:
    return inventory["establishment_year"] < rollback_year


def establishment_sr_disturbance(
    disturbances: dict[str, np.ndarray], establishment_year: int
) -> bool:
    return np.logical_and(
        disturbances["year"] == establishment_year,
        disturbances["is_stand_replacing"],
    ).any()


def deforestation_present(disturbances: dict[str, np.ndarray]):
    return disturbances["is_deforestation"].any()


class WorkUnitFacts:
    def __init__(
        self,
        inventory: dict,
        disturbance: dict[str, np.ndarray],
        rollback_year: int,
        inventory_year: int,
    ):
        self._null_inventory = null_inventory(inventory)
        self._rollback_period_sr_disturbance_count = (
            rollback_period_sr_disturbances_count(
                disturbance, rollback_year, inventory_year
            )
        )
        self._rollback_period_sr_disturbances = (
            self._rollback_period_sr_disturbance_count > 0
        )
        self._pre_rollback_sr_disturbances = pre_rollback_sr_disturbances(
            disturbance, rollback_year
        )
        self._pre_est_post_rollback_sr_disturbances = (
            pre_est_post_rollback_sr_disturbances(
                disturbance, rollback_year, inventory["establishment_year"]
            )
        )
        self._sr_disturbance_after_establishment = (
            sr_disturbance_after_establishment(
                disturbance, inventory["establishment_year"], inventory_year
            )
        )
        self._establishment_before_rollback = establishment_before_rollback(
            inventory, rollback_year
        )
        self._establishment_sr_disturbance = establishment_sr_disturbance(
            disturbance, inventory["establishment_year"]
        )
        self._deforestation_present = deforestation_present(disturbance)

    @property
    def null_inventory(self) -> bool:
        """
        return true if the work unit inventory is null, otherwise false
        """
        return self._null_inventory

    @property
    def rollback_period_sr_disturbance_count(self) -> int:
        return self._rollback_period_sr_disturbance_count

    @property
    def rollback_period_sr_disturbances(self) -> bool:
        """
        return true if one or more stand replacing disturbance occurs in the
        period between the rollback year and the inventory year, otherwise
        false
        """
        return self._rollback_period_sr_disturbances

    @property
    def pre_rollback_sr_disturbances(self) -> bool:
        """
        Returns true if at least one stand replacing disturbance occurs
        before the rollback year, otherwise false
        """
        return self._pre_rollback_sr_disturbances

    @property
    def pre_est_post_rollback_sr_disturbances(self) -> bool:
        """
        returns true if at least one stand replacing disturbance occurs on
        or after the rollback year and prior to or on the inventory
        establishment year, otherwise false
        """

        return self._pre_est_post_rollback_sr_disturbances

    @property
    def sr_disturbance_after_establishment(self) -> bool:
        """
        returns true if one or more stand replacing disturbances occur after
        inventory establishment year and prior to the inventory vintage year,
        otherwise false
        """
        return self._sr_disturbance_after_establishment

    @property
    def establishment_before_rollback(self) -> bool:
        """
        returns true if the inventory establishment year occurs before the
        rollback year, otherwise false
        """
        return self._establishment_before_rollback

    @property
    def establishment_sr_disturbance(self) -> bool:
        """
        returns true if one or more disturbances occur on the inventory
        establishment year, otherwise false
        """
        return self._establishment_sr_disturbance

    @property
    def deforestation_present(self) -> bool:
        """
        returns true if one or more deforestation disturbances occur, otherwise
        false
        """
        return self._deforestation_present

    def get_fact_values(self) -> dict[str, Union[bool, int]]:
        return {
            k: v.__get__(self) for k, v in WORK_UNIT_FACT_PROPERTIES.items()
        }


WORK_UNIT_FACT_PROPERTIES: dict[str, property] = {
    k: v for k, v in vars(WorkUnitFacts).items() if type(v) is property
}
