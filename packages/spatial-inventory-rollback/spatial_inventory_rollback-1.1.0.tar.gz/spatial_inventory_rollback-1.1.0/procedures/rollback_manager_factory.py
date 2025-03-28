from typing import Union
from spatial_inventory_rollback.procedures.no_supporting_info_rollback_procedure import (  # noqa 503
    NoSupportingInfoRollbackProcedure,
)
from spatial_inventory_rollback.procedures.regen_delay_rollback_procedure import (  # noqa 503
    RegenDelayRollbackProcedure,
)
from spatial_inventory_rollback.procedures.distribution_age_generator import (
    DistributionAgeGenerator,
)
from spatial_inventory_rollback.procedures import (
    categorical_distribution_index,
)
from spatial_inventory_rollback.procedures.rollback_manager import (
    RollbackManager,
)
from spatial_inventory_rollback.procedures.basic_rollback_procedure import (
    BasicRollbackProcedure,
)
from spatial_inventory_rollback.procedures.shift_disturbance_procedure import (
    ShiftDisturbanceProcedure,
)
from spatial_inventory_rollback.procedures.shift_establishment_procedure import (  # noqa 503
    ShiftEstablishmentProcedure,
)
from spatial_inventory_rollback.procedures.nodata_rollback_procedure import (
    NoDataRollbackProcedure,
)
from spatial_inventory_rollback.procedures.work_unit_facts import (
    WORK_UNIT_FACT_PROPERTIES,
)
from spatial_inventory_rollback.operating_format.attribute_layer import (
    AttributeLayer,
)
from spatial_inventory_rollback.operating_format.landscape import Landscape
from spatial_inventory_rollback.procedures.disturbance_type_generator import (
    DisturbanceTypeGenerator,
)


def get_rollback_manager(
    rollback_year: int,
    age_class_distribution: Union[str, list[dict]],
    prioritize_disturbances: bool,
    landscape: Landscape,
    disturbance_type_generator_config: Union[str, list[dict]],
    single_draw: bool = False,
    **kwargs
):
    age_generator = DistributionAgeGenerator(
        categorical_distribution_index.load_distribution_config(
            age_class_distribution, expand_distribution=True
        ),
        single_draw=single_draw,
    )
    disturbance_type_generator = DisturbanceTypeGenerator(
        categorical_distribution_index.load_distribution_config(
            disturbance_type_generator_config
        ),
    )
    rollback_manager = RollbackManager(
        rollback_year=rollback_year,
        rollback_procedures=[
            NoDataRollbackProcedure(),
            BasicRollbackProcedure(disturbance_type_generator, **kwargs),
            NoSupportingInfoRollbackProcedure(
                age_generator, disturbance_type_generator, **kwargs
            ),
            RegenDelayRollbackProcedure(
                age_generator, disturbance_type_generator, **kwargs
            ),
            ShiftDisturbanceProcedure(
                age_generator,
                prioritize_disturbances,
                disturbance_type_generator,
                **kwargs
            ),
            ShiftEstablishmentProcedure(
                age_generator,
                prioritize_disturbances,
                disturbance_type_generator,
                **kwargs
            ),
        ],
        procedure_info_layer=create_procedure_info_layer(landscape),
    )

    return rollback_manager


def create_procedure_info_layer(landscape: Landscape):
    procedure_info_layer_cols = ["procedure_name", "procedure_description"]
    procedure_info_layer_cols.extend(WORK_UNIT_FACT_PROPERTIES.keys())
    return AttributeLayer(
        landscape.stack_bounds,
        name="procedures",
        unique=True,
        columns=procedure_info_layer_cols,
    )
