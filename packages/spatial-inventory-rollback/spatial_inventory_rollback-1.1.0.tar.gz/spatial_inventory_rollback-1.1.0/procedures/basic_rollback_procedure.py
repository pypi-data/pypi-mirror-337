from spatial_inventory_rollback.procedures.rollback_procedure import (
    RollbackProcedure,
)
from spatial_inventory_rollback.operating_format.rollback_output import (
    RollbackOutput,
)
from spatial_inventory_rollback.procedures.procedure_work_unit import (
    ProcedureWorkUnit,
)
import numpy as np
from spatial_inventory_rollback.procedures import work_unit_functions
from spatial_inventory_rollback.procedures import deforestation_pre_process
from spatial_inventory_rollback.procedures.deforestation_pre_process import (
    PreprocesResult,
)
from spatial_inventory_rollback.procedures import procedure_descriptions
from spatial_inventory_rollback.procedures.disturbance_type_generator import (
    DisturbanceTypeGenerator,
)


class BasicRollbackProcedure(RollbackProcedure):
    def __init__(
        self,
        disturbance_type_generator: DisturbanceTypeGenerator,
        *args,
        **kwargs
    ):
        """The simplest possible rollback procedure for work units with no
        contradictory disturbances and an establishment year earlier than the
        rollback year. In this case, the rollback age is the rollback year
        minus the establishment year.
        """
        super().__init__(*args, **kwargs)
        self._disturbance_type_generator = disturbance_type_generator

    def can_rollback(self, work_unit: ProcedureWorkUnit):
        return work_unit.facts.establishment_before_rollback

    def get_procedure_description(self, work_unit: ProcedureWorkUnit) -> str:
        has_contradictory_disturbance = (
            work_unit.facts.rollback_period_sr_disturbances
        )
        has_old_disturbance = work_unit.facts.pre_rollback_sr_disturbances

        return (
            procedure_descriptions.ROLLBACK_CASE_02_AND_03
            if has_old_disturbance and has_contradictory_disturbance
            else procedure_descriptions.ROLLBACK_CASE_02
            if has_old_disturbance
            else procedure_descriptions.ROLLBACK_CASE_03
            if has_contradictory_disturbance
            else procedure_descriptions.ROLLBACK_CASE_01
        )

    def rollback(
        self,
        work_unit: ProcedureWorkUnit,
        rollback_year: int,
        rollback_output: RollbackOutput,
    ):
        # Handle any last-pass disturbance events: must have at least one event
        # at the establishment year plus any number of pre-establishment events
        # that the user might have provided. If no establishment event exists,
        # create one using the most recent pre-rollback disturbance type or the
        # default establishment disturbance type.

        deforestation_result = deforestation_pre_process.pre_process(
            work_unit, rollback_year
        )

        if deforestation_result == PreprocesResult.PreTransitionPeriod:
            return  # stand is permanently deforested

        inventory = work_unit.layer_data["gcbm_inventory"]
        disturbance = work_unit.layer_data["gcbm_disturbance"]

        if deforestation_result == PreprocesResult.NoDeforestation:
            rollback_establishment_year = (
                work_unit_functions.compute_rollback_establishment_year(
                    inventory, disturbance, rollback_year
                )
            )
            inventory["establishment_year"] = rollback_establishment_year
            inventory["delay"] = 0

        rollback_output.set_inventory(work_unit.indices, inventory)
        keep_events = work_unit_functions.filter_events(
            disturbance,
            np.logical_or(
                disturbance["year"] >= rollback_year,
                np.logical_and(
                    disturbance["year"] <= inventory["establishment_year"],
                    disturbance["is_stand_replacing"],
                ),
            ),
        )
        out_events = rollback_output.create_output_events()
        out_events.append_events(keep_events)

        if (
            not work_unit.facts.establishment_sr_disturbance
            and not deforestation_result == PreprocesResult.PreRollback
        ):
            # need to add an establishment event if there was neither a
            # historic SR disturbance that falls on the establishment year,
            # nor a historical deforestation event
            if work_unit.facts.pre_rollback_sr_disturbances:
                most_recent_sr_dist_idx = (
                    work_unit_functions.get_matching_year_index(
                        year_array=disturbance["year"],
                        year_bound_inclusive=rollback_year - 1,
                        include_mask=disturbance["is_stand_replacing"],
                        most_recent=True,
                    )
                )
                establishment_dist_type = disturbance["disturbance_type"][
                    most_recent_sr_dist_idx
                ]
            else:
                random_dist_type_key = inventory.copy()
                random_dist_type_key["disturbance_year"] = inventory[
                    "establishment_year"
                ]
                establishment_dist_type = self._disturbance_type_generator.get_random_disturbance_type(  # noqa: E501
                    random_dist_type_key
                )

            out_events.append_events(
                {
                    "year": inventory["establishment_year"],
                    "disturbance_type": establishment_dist_type,
                    "is_stand_replacing": True,
                }
            )

        rollback_output.set_disturbances(work_unit.indices, out_events)
