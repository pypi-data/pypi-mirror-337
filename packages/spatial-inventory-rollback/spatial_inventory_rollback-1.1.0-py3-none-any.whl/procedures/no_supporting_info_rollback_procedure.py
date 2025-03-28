import numpy as np
from spatial_inventory_rollback.procedures.rollback_procedure import (
    RollbackProcedure,
)
from spatial_inventory_rollback.procedures.procedure_work_unit import (
    ProcedureWorkUnit,
)
from spatial_inventory_rollback.operating_format.rollback_output import (
    RollbackOutput,
)
from spatial_inventory_rollback.procedures import work_unit_functions
from spatial_inventory_rollback.procedures import random_events
from spatial_inventory_rollback.procedures.age_generator import AgeGenerator
from spatial_inventory_rollback.procedures.disturbance_type_generator import (
    DisturbanceTypeGenerator,
)
from spatial_inventory_rollback.procedures import procedure_descriptions


class NoSupportingInfoRollbackProcedure(RollbackProcedure):
    def __init__(
        self,
        age_generator: AgeGenerator,
        disturbance_type_generator: DisturbanceTypeGenerator,
        *args,
        **kwargs
    ):
        """Rollback procedure for work units with an establishment year later
        than the rollback year and no post-rollback disturbance information.
        If no pre-rollback SR disturbance is defined, the rollback procedure
        draws a new initial age from the provided generator, and creates a
        disturbance event in the rollback period to match the original
        inventory age.  If a pre-rollback SR is defined, a regeneration delay
        spanning the years between the pre-rollback-SR and the inventory
        establishment year is added

        Args:
            age_generator (AgeGenerator): generates a new initial age for work
                units with no supporting disturbance information.
        """
        super().__init__(*args, **kwargs)
        self._age_generator = age_generator
        self._disturbance_type_generator = disturbance_type_generator

    def can_rollback(self, work_unit: ProcedureWorkUnit) -> bool:
        return (
            not work_unit.facts.establishment_before_rollback
            and not work_unit.facts.rollback_period_sr_disturbances
        )

    def get_procedure_description(self, work_unit: ProcedureWorkUnit) -> str:
        return (
            procedure_descriptions.ROLLBACK_CASE_04b
            if work_unit.facts.pre_rollback_sr_disturbances
            else procedure_descriptions.ROLLBACK_CASE_04a
        )

    def rollback(
        self,
        work_unit: ProcedureWorkUnit,
        rollback_year: int,
        rollback_output: RollbackOutput,
    ):
        gcbm_inventory = work_unit.get_layer("gcbm_inventory")
        disturbance_layer = work_unit.get_layer("gcbm_disturbance")

        output_events = rollback_output.create_output_events()

        # keep all existing events except for historic
        # non stand replacing events
        output_events.append_events(
            work_unit_functions.filter_events(
                disturbance_layer,
                included=~np.logical_and(
                    disturbance_layer["year"] < rollback_year,
                    ~disturbance_layer["is_stand_replacing"],
                ),
            )
        )

        # If disturbance data includes at least one stand-replacing event
        # before the rollback year, set a regeneration delay
        year_of_most_recent_pre_rollback_sr = (
            work_unit_functions.compute_rollback_establishment_year(
                gcbm_inventory, disturbance_layer, rollback_year
            )
        )
        if year_of_most_recent_pre_rollback_sr:
            rollback_output.set_disturbances(work_unit.indices, output_events)
            # by convention an age of -N will indicate to regen delay N years
            # after spinup, since the establishment year is > the rollback
            # year in this procedure, the age will be a negative value

            gcbm_inventory["delay"] = (
                rollback_year - year_of_most_recent_pre_rollback_sr
            )
            rollback_output.set_inventory(work_unit.indices, gcbm_inventory)
            return

        # add an event at the establishment year
        random_dist_type_key = gcbm_inventory.copy()
        random_dist_type_key["disturbance_year"] = random_dist_type_key[
            "establishment_year"
        ]
        establishment_dist_type = (
            self._disturbance_type_generator.get_random_disturbance_type(
                random_dist_type_key
            )
        )
        output_events.append_events(
            {
                "year": gcbm_inventory["establishment_year"],
                "disturbance_type": establishment_dist_type,
                "is_stand_replacing": True,
            }
        )

        # No pre-rollback disturbances: draw from distribution until the
        # rollback year is reached.
        historic_rollback_years = (
            gcbm_inventory["establishment_year"] - rollback_year
        )
        age_distribution_key = gcbm_inventory.copy()
        age_distribution_key.update(
            {
                "inventory_year": int(age_distribution_key["inventory_year"]),
                "establishment_year": int(
                    age_distribution_key["establishment_year"]
                ),
                "disturbance_type": establishment_dist_type,
                "disturbance_year": int(gcbm_inventory["establishment_year"]),
            }
        )
        random_age_draws = self._age_generator.assign(
            work_unit=work_unit,
            distribution_key=age_distribution_key,
            min_years=historic_rollback_years,
        ).cumsum(axis=1)
        random_events.add_random_events(
            random_age_draws=random_age_draws,
            work_unit=work_unit,
            rollback_output=rollback_output,
            establishment_year=gcbm_inventory["establishment_year"],
            classifier_value_key=gcbm_inventory,
            disturbance_type_generator=self._disturbance_type_generator,
            output_events=output_events,
        )

        establishment_year = gcbm_inventory["establishment_year"] - np.nanmax(
            random_age_draws, axis=1
        )
        gcbm_inventory["establishment_year"] = establishment_year
        rollback_output.set_inventory(work_unit.indices, gcbm_inventory)
