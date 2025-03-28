import numpy as np
from spatial_inventory_rollback.procedures.rollback_procedure import (
    RollbackProcedure,
)
from spatial_inventory_rollback.procedures import work_unit_functions
from spatial_inventory_rollback.procedures import random_events
from spatial_inventory_rollback.operating_format.rollback_output import (
    RollbackOutput,
)
from spatial_inventory_rollback.procedures.procedure_work_unit import (
    ProcedureWorkUnit,
)
from spatial_inventory_rollback.procedures.age_generator import AgeGenerator
from spatial_inventory_rollback.procedures import procedure_descriptions
from spatial_inventory_rollback.procedures.disturbance_type_generator import (
    DisturbanceTypeGenerator,
)


class RegenDelayRollbackProcedure(RollbackProcedure):
    def __init__(
        self,
        age_generator: AgeGenerator,
        disturbance_type_generator: DisturbanceTypeGenerator,
        *args,
        **kwargs
    ):
        """Rollback procedure for work units with an establishment year later
        than the rollback year, no disturbance information for the pre-rollback
        period, with at least one disturbance between the rollback and
        inventory years but none after the establishment year. In this case,
        the rollback procedure draws the new initial age from the provided
        generator, and keeps the disturbances in the rollback period, adding a
        regen delay to the final event if necessary to make it consistent with
        the original inventory age.

        Args:
            age_generator (AgeGenerator): generates a new initial age for work
                units with no supporting disturbance information.
        """
        super().__init__(*args, **kwargs)
        self._age_generator = age_generator
        self._disturbance_type_generator = disturbance_type_generator

    def can_rollback(self, work_unit: ProcedureWorkUnit):
        return (
            not work_unit.facts.establishment_before_rollback
            and work_unit.facts.pre_est_post_rollback_sr_disturbances
            and not work_unit.facts.sr_disturbance_after_establishment
            and not work_unit.facts.deforestation_present
        )

    def get_procedure_description(self, work_unit: ProcedureWorkUnit) -> str:
        if work_unit.facts.pre_rollback_sr_disturbances:
            if work_unit.facts.establishment_sr_disturbance:
                return procedure_descriptions.ROLLBACK_CASE_05b
            else:
                return procedure_descriptions.ROLLBACK_CASE_06b
        else:
            if work_unit.facts.establishment_sr_disturbance:
                return procedure_descriptions.ROLLBACK_CASE_05a
            else:
                return procedure_descriptions.ROLLBACK_CASE_06a

    def rollback(
        self,
        work_unit: ProcedureWorkUnit,
        rollback_year: int,
        rollback_output: RollbackOutput,
    ):
        gcbm_inventory = work_unit.get_layer("gcbm_inventory")
        disturbance_layer = work_unit.get_layer("gcbm_disturbance")

        first_rollback_dist_idx = work_unit_functions.get_matching_year_index(
            year_array=disturbance_layer["year"],
            year_bound_inclusive=rollback_year,
            include_mask=disturbance_layer["is_stand_replacing"],
            most_recent=False,
        )

        last_rollback_dist_idx = work_unit_functions.get_matching_year_index(
            year_array=disturbance_layer["year"],
            year_bound_inclusive=gcbm_inventory["establishment_year"],
            include_mask=disturbance_layer["is_stand_replacing"],
            most_recent=True,
        )

        output_events = rollback_output.create_output_events()

        regen_delay = gcbm_inventory["establishment_year"] - int(
            disturbance_layer["year"][last_rollback_dist_idx]
        )
        disturbance_layer["regen_delay"][last_rollback_dist_idx] = regen_delay
        disturbance_layer["age_after"][last_rollback_dist_idx] = 0

        if not work_unit.facts.pre_rollback_sr_disturbances:
            # filter out pre-rollback year non-stand-replacing disturbances
            # when the age and historic disturbance events need to be
            # generated.
            output_events.append_events(
                work_unit_functions.filter_events(
                    disturbance_layer,
                    included=~np.logical_and(
                        disturbance_layer["year"] < rollback_year,
                        ~disturbance_layer["is_stand_replacing"],
                    ),
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
        else:
            rollback_establishment_year = (
                work_unit_functions.compute_rollback_establishment_year(
                    gcbm_inventory, disturbance_layer, rollback_year
                )
            )
            output_events.append_events(disturbance_layer)
            rollback_output.set_disturbances(work_unit.indices, output_events)
            gcbm_inventory["establishment_year"] = rollback_establishment_year
            rollback_output.set_inventory(work_unit.indices, gcbm_inventory)
