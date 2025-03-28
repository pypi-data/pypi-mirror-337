import numpy as np
from spatial_inventory_rollback.operating_format.landscape import (
    LandscapeWorkUnit,
)
from spatial_inventory_rollback.procedures.work_unit_facts import WorkUnitFacts


class ProcedureWorkUnit(LandscapeWorkUnit):
    def __init__(
        self,
        indices: np.ndarray,
        layer_data: dict,
        work_unit_facts: WorkUnitFacts,
    ):
        super().__init__(indices, layer_data)

        self._facts = work_unit_facts

    @property
    def facts(self) -> WorkUnitFacts:
        return self._facts


def create_procedure_work_unit(
    work_unit: LandscapeWorkUnit, rollback_year: int
):
    inventory = work_unit.get_layer("gcbm_inventory")
    work_unit_facts = WorkUnitFacts(
        inventory=inventory,
        disturbance=work_unit.get_layer("gcbm_disturbance"),
        rollback_year=rollback_year,
        inventory_year=inventory["inventory_year"],
    )
    return ProcedureWorkUnit(
        work_unit.indices, work_unit.layer_data, work_unit_facts
    )
