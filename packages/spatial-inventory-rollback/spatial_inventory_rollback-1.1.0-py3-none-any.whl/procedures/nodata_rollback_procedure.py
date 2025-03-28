from spatial_inventory_rollback.procedures.rollback_procedure import (
    RollbackProcedure,
)
from spatial_inventory_rollback.procedures.procedure_work_unit import (
    ProcedureWorkUnit,
)
from spatial_inventory_rollback.operating_format.rollback_output import (
    RollbackOutput,
)
from spatial_inventory_rollback.procedures import procedure_descriptions


class NoDataRollbackProcedure(RollbackProcedure):
    def __init__(self, *args, **kwargs):
        """No-op rollback procedure that matches pixels with a null
        establishment year and doesn't do any work.
        """
        super().__init__(*args, **kwargs)

    def can_rollback(self, work_unit: ProcedureWorkUnit):
        return work_unit.facts.null_inventory

    def get_procedure_description(self, work_unit: ProcedureWorkUnit) -> str:
        return procedure_descriptions.ROLLBACK_CASE_00

    def rollback(
        self,
        work_unit: ProcedureWorkUnit,
        rollback_year: int,
        rollback_output: RollbackOutput,
    ):
        pass
