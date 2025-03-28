from __future__ import annotations
from spatial_inventory_rollback.application import log_helper

from spatial_inventory_rollback.operating_format.rollback_output import (
    RollbackOutput,
)

from spatial_inventory_rollback.operating_format.landscape import Landscape
from spatial_inventory_rollback.procedures.rollback_procedure import (
    RollbackProcedure,
)
from spatial_inventory_rollback.procedures import procedure_work_unit
from spatial_inventory_rollback.procedures.procedure_work_unit import (
    ProcedureWorkUnit,
)
from spatial_inventory_rollback.operating_format.attribute_layer import (
    AttributeLayer,
)
from spatial_inventory_rollback.procedures.work_unit_facts import (
    WORK_UNIT_FACT_PROPERTIES,
)
import pandas as pd

logger = log_helper.get_logger()


class RollbackManager:
    def __init__(
        self,
        rollback_year: int,
        rollback_procedures: list[RollbackProcedure],
        procedure_info_layer: AttributeLayer,
    ):
        """Rolls a landscape back to a specified year using an eligible
        rollback procedure from a list of possibilities for each work unit.

        Args:
            rollback_year (int): the year to roll back to.
            rollback_procedures (list of RollbackProcedure objects): one or
                more rollback procedures that handle specific conditions
                encountered in the landscape's work units.
            procedure_info_layer (AttributeLayer): diagnostic layer for
                spatially tracking the rollback procedures, procedure
                descriptions, and work_unit facts for the rollback process
        """
        self._rollback_year = rollback_year
        self._rollback_procedures = rollback_procedures
        self._procedure_info_layer = procedure_info_layer
        self._multiple_matching_procedures: dict[tuple, set[str]] = {}

    @property
    def procedure_info_layer(self) -> AttributeLayer:
        return self._procedure_info_layer

    def get_multiple_matching_procedures(self) -> pd.DataFrame:
        """Gets a summarized dataframe of work unit facts and their multiple
        eligible procedures, if any
        """
        work_unit_fact_names = list(WORK_UNIT_FACT_PROPERTIES.keys())
        data = []
        columns = work_unit_fact_names + ["procedures"]
        if len(self._multiple_matching_procedures):
            return pd.DataFrame(columns=columns)
        for k, v in self._multiple_matching_procedures.items():
            row_data = {
                col: k[i] for i, col in enumerate(work_unit_fact_names)
            }
            row_data.update(", ".join(v))
            data.append(row_data)
        return pd.DataFrame(columns=columns, data=data)

    def _find_procedure(self, work_unit: ProcedureWorkUnit):
        found_procedure: RollbackProcedure = None
        for procedure in self._rollback_procedures:
            if procedure.can_rollback(work_unit):
                if found_procedure is not None:
                    multiple_matches_key = tuple(
                        work_unit.facts.get_fact_values().values()
                    )
                    if (
                        multiple_matches_key
                        in self._multiple_matching_procedures
                    ):
                        self._multiple_matching_procedures[
                            multiple_matches_key
                        ].add(type(procedure).__name__)
                    else:
                        self._multiple_matching_procedures[
                            multiple_matches_key
                        ] = set([type(procedure).__name__])
                else:
                    found_procedure = procedure

        if not found_procedure:
            raise RuntimeError(
                "Can't find procedure to perform rollback. "
                f"Work unit: {work_unit.layer_data}"
            )
        return found_procedure

    def rollback(self, landscape: Landscape) -> RollbackOutput:
        """Rolls the specified landscape back based on the manager's configured
        rollback year and procedures.

        Args:
            landscape (Landscape): the landscape to roll back.

        Returns:
            RollbackOutput: an instance of Rollback output containing the
                rolled back disturbance and inventory information.
        """
        rollback_output = RollbackOutput(landscape, self._rollback_year)
        logger.info("rollback process start")

        count_processed = 0
        for landscape_work_unit in landscape.get_work_units():
            work_unit = procedure_work_unit.create_procedure_work_unit(
                landscape_work_unit, self._rollback_year
            )

            procedure = self._find_procedure(work_unit)

            self._append_procedure_info(work_unit, procedure)

            procedure.rollback(work_unit, self._rollback_year, rollback_output)

            count_processed += 1

        logger.info(f"processed {count_processed} rollback cases")

        return rollback_output

    def _append_procedure_info(
        self, work_unit: ProcedureWorkUnit, procedure: RollbackProcedure
    ):
        procedure_info_layer_values = [
            procedure.__class__.__name__,
            procedure.get_procedure_description(work_unit),
        ]
        procedure_info_layer_values.extend(
            work_unit.facts.get_fact_values().values()
        )

        self._procedure_info_layer.set_data(
            work_unit.indices,
            tuple(procedure_info_layer_values),
        )
