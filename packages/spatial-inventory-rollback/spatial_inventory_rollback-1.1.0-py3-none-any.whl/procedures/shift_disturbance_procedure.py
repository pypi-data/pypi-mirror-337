import numpy as np
from spatial_inventory_rollback.procedures.rollback_procedure import (
    RollbackProcedure,
)
from spatial_inventory_rollback.procedures import work_unit_functions
from spatial_inventory_rollback.procedures import random_events
from spatial_inventory_rollback.procedures import deforestation_pre_process
from spatial_inventory_rollback.procedures.deforestation_pre_process import (
    PreprocesResult,
)
from spatial_inventory_rollback.operating_format.rollback_output import (
    RollbackOutput,
)
from spatial_inventory_rollback.procedures.procedure_work_unit import (
    ProcedureWorkUnit,
)
from spatial_inventory_rollback.procedures.age_generator import AgeGenerator
from spatial_inventory_rollback.procedures.disturbance_type_generator import (
    DisturbanceTypeGenerator,
)
from spatial_inventory_rollback.procedures import procedure_descriptions


class ShiftDisturbanceProcedure(RollbackProcedure):
    """Rollback procedure for work units with an establishment year later than
    the rollback year. The event nearest to the inventory establishment year
    is shifted to the inventory establishment year. If after the shift is
    performed any stand replacing events remain after the establishment year
    they will be dropped.

    Args:
        age_generator (AgeGenerator): generates a new initial age for work
            units with no supporting disturbance information.
        prioritize_disturbance (bool): if set to false this procedure is
            enabled, and if true disabled.
        inventory_year (int): the inventory vintage

    """

    def __init__(
        self,
        age_generator: AgeGenerator,
        prioritize_disturbance: bool,
        disturbance_type_generator: DisturbanceTypeGenerator,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self._age_generator = age_generator
        self._prioritize_disturbance = prioritize_disturbance
        self._disturbance_type_generator = disturbance_type_generator

    def can_rollback(self, work_unit: ProcedureWorkUnit):
        return (
            not work_unit.facts.establishment_before_rollback
            and (
                work_unit.facts.sr_disturbance_after_establishment
                or work_unit.facts.deforestation_present
            )
            and not self._prioritize_disturbance
        )

    def get_procedure_description(self, work_unit: ProcedureWorkUnit) -> str:
        if work_unit.facts.pre_rollback_sr_disturbances:
            if work_unit.facts.rollback_period_sr_disturbance_count == 1:
                return procedure_descriptions.ROLLBACK_CASE_07b
            else:
                return procedure_descriptions.ROLLBACK_CASE_09b
        else:
            if work_unit.facts.rollback_period_sr_disturbance_count > 1:
                return procedure_descriptions.ROLLBACK_CASE_07a
            else:
                return procedure_descriptions.ROLLBACK_CASE_09a

    def rollback(
        self,
        work_unit: ProcedureWorkUnit,
        rollback_year: int,
        rollback_output: RollbackOutput,
    ):
        deforestation_result = deforestation_pre_process.pre_process(
            work_unit, rollback_year
        )

        if deforestation_result == PreprocesResult.PreTransitionPeriod:
            return  # stand is permanently deforested

        gcbm_inventory = work_unit.get_layer("gcbm_inventory")
        disturbance_layer = work_unit.get_layer("gcbm_disturbance")
        output_events = rollback_output.create_output_events()

        if deforestation_result == PreprocesResult.PostRollback:
            # since we will be shifting back the deforestation event, which
            # is the most recent SR event (the return value of
            # PreprocesResult.PostRollback gaurantees that), we need to delete
            # all *other* events between the inventory establishment year and
            # the deforestation year
            i_recent_deforestation = (
                work_unit_functions.get_nearest_year_index(
                    year_array=disturbance_layer["year"],
                    year_target=gcbm_inventory["inventory_year"],
                    include_mask=disturbance_layer["is_deforestation"],
                    first_match=False,
                )
            )
            year_recent_deforestation = disturbance_layer["year"][
                i_recent_deforestation
            ]

            exclude_filter = np.logical_and(
                disturbance_layer["year"]
                >= gcbm_inventory["establishment_year"],
                disturbance_layer["year"] < year_recent_deforestation,
            )

            # shift the deforestation event
            disturbance_layer["year"][i_recent_deforestation] = gcbm_inventory[
                "establishment_year"
            ]

        elif not deforestation_result == PreprocesResult.PreRollback:
            # 1. find the stand replacing disturbance closest to the inventory
            #    establishment
            i_closest = work_unit_functions.get_nearest_year_index(
                year_array=disturbance_layer["year"],
                year_target=gcbm_inventory["establishment_year"],
                include_mask=np.logical_and(
                    disturbance_layer["is_stand_replacing"],
                    disturbance_layer["year"] > rollback_year,
                ),
                first_match=True,
            )

            # 2. shift that disturbance to the inventory year
            disturbance_layer["year"][i_closest] = gcbm_inventory[
                "establishment_year"
            ]

            # 3. discard all remaining stand replacing events that are after
            #    the inventory establishment and before the inventory year
            exclude_filter = np.logical_and(
                np.logical_and(
                    disturbance_layer["year"]
                    > gcbm_inventory["establishment_year"],
                    disturbance_layer["year"]
                    <= gcbm_inventory["inventory_year"],
                ),
                disturbance_layer["is_stand_replacing"],
            )

        if deforestation_result == PreprocesResult.PreRollback:
            # rollback pre-process already set the values for inventory
            # age/delay
            rollback_output.set_inventory(work_unit.indices, gcbm_inventory)
            output_events.append_events(disturbance_layer)
            rollback_output.set_disturbances(work_unit.indices, output_events)

        elif work_unit.facts.pre_rollback_sr_disturbances:
            rollback_establishment_year = (
                work_unit_functions.compute_rollback_establishment_year(
                    gcbm_inventory, disturbance_layer, rollback_year
                )
            )
            output_events.append_events(
                work_unit_functions.filter_events(
                    disturbance_layer, included=~exclude_filter
                )
            )
            rollback_output.set_disturbances(work_unit.indices, output_events)
            gcbm_inventory["establishment_year"] = rollback_establishment_year
            rollback_output.set_inventory(work_unit.indices, gcbm_inventory)
        else:
            # 3a. additionally exclude all pre-rollback NSRs if the tool will
            # be randomly generating historic SR disturbances
            exclude_filter = np.logical_or(
                exclude_filter,
                np.logical_and(
                    ~disturbance_layer["is_stand_replacing"],
                    disturbance_layer["year"] < rollback_year,
                ),
            )
            output_events.append_events(
                work_unit_functions.filter_events(
                    disturbance_layer, included=~exclude_filter
                )
            )

            # 4. find the closest-to-rollback post-rollback year stand
            # replacing disturbance; the disturbance type potentially matters
            # to the age distribution.
            first_rollback_dist_idx = (
                work_unit_functions.get_nearest_year_index(
                    year_array=disturbance_layer["year"],
                    year_target=rollback_year,
                    include_mask=disturbance_layer["is_stand_replacing"],
                    first_match=True,
                )
            )
            first_rollback_dist_year = int(
                disturbance_layer["year"][first_rollback_dist_idx]
            )
            first_rollback_dist_type = str(
                disturbance_layer["disturbance_type"][first_rollback_dist_idx]
            )
            historic_rollback_years = first_rollback_dist_year - rollback_year
            distribution_key = gcbm_inventory.copy()
            distribution_key.update(
                {
                    "inventory_year": int(distribution_key["inventory_year"]),
                    "establishment_year": int(
                        distribution_key["establishment_year"]
                    ),
                    "disturbance_type": first_rollback_dist_type,
                    "disturbance_year": first_rollback_dist_year,
                }
            )
            random_age_draws = self._age_generator.assign(
                work_unit=work_unit,
                distribution_key=distribution_key,
                min_years=historic_rollback_years,
            ).cumsum(axis=1)

            random_events.add_random_events(
                random_age_draws=random_age_draws,
                work_unit=work_unit,
                rollback_output=rollback_output,
                establishment_year=first_rollback_dist_year,
                classifier_value_key=gcbm_inventory,
                disturbance_type_generator=self._disturbance_type_generator,
                output_events=output_events,
            )
            rollback_establishment_year = first_rollback_dist_year - np.nanmax(
                random_age_draws, axis=1
            )
            gcbm_inventory["establishment_year"] = rollback_establishment_year
            rollback_output.set_inventory(work_unit.indices, gcbm_inventory)
