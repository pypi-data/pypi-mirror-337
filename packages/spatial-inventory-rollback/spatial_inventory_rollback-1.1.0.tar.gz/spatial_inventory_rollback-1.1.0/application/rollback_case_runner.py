from __future__ import annotations
import numpy as np
import pandas as pd

from spatial_inventory_rollback.procedures.rollback_manager import (
    RollbackManager,
)
from spatial_inventory_rollback.procedures.rollback_manager_factory import (
    create_procedure_info_layer,
)
from spatial_inventory_rollback.procedures.distribution_age_generator import (
    DistributionAgeGenerator,
)
from spatial_inventory_rollback.procedures.disturbance_type_generator import (
    DisturbanceTypeGenerator,
)
from spatial_inventory_rollback.procedures import (
    categorical_distribution_index,
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
from spatial_inventory_rollback.procedures.no_supporting_info_rollback_procedure import (  # noqa 503
    NoSupportingInfoRollbackProcedure,
)
from spatial_inventory_rollback.procedures.regen_delay_rollback_procedure import (  # noqa 503
    RegenDelayRollbackProcedure,
)

from spatial_inventory_rollback.operating_format.layer import Layer

from spatial_inventory_rollback.raster.raster_bound import RasterBound
from spatial_inventory_rollback.operating_format.landscape import Landscape


class CaseRunnerLayer(Layer):
    def __init__(
        self,
        name,
        layer_data,
        layer_attributes,
        single_value,
        classifier_names,
    ):
        self._bounds = RasterBound(
            0, 0, layer_data.shape[0], layer_data.shape[1]
        )
        self._layer_data = layer_data
        self._layer_attributes = layer_attributes
        self._name = name
        self._single_value = single_value
        self._classifier_names = classifier_names
        self._classifier_info = {
            c: {"attributes": {}} for c in self._classifier_names
        }

    @property
    def nodata(self) -> int:
        return 0

    @property
    def classifier_info(self) -> dict:
        return self._classifier_info

    @property
    def name(self) -> str:
        return self._name

    @property
    def classifier_names(self) -> str:
        return self._classifier_names

    @property
    def path(self) -> str:
        raise NotImplementedError()

    @property
    def bounds(self) -> RasterBound:
        return self._bounds

    @property
    def stack_bounds(self) -> RasterBound:
        return self._bounds

    @property
    def layer_data(self) -> np.ndarray:
        return self._layer_data

    def flatten(self):
        self._layer_data = self._layer_data.flatten()

    def select_data(self, layer_id: int):
        match_rows = self._layer_attributes[
            self._layer_attributes.id == layer_id
        ]
        if self._single_value:
            return {col: match_rows[col].iloc[0] for col in match_rows.columns}
        return {col: match_rows[col].to_numpy() for col in match_rows.columns}

    def select_all(self) -> pd.DataFrame:
        raise NotImplementedError()


def get_rollback_manager(
    landscape,
    rollback_year,
    age_class_distribution,
    prioritize_disturbances,
    single_draw,
    disturbance_type_generator_config,
):
    age_generator = DistributionAgeGenerator(
        categorical_distribution_index.load_distribution_config(
            age_class_distribution
        ),
        single_draw=single_draw,
    )

    disturbance_type_generator = DisturbanceTypeGenerator(
        categorical_distribution_index.load_distribution_config(
            disturbance_type_generator_config
        ),
    )
    return RollbackManager(
        rollback_year=rollback_year,
        rollback_procedures=[
            NoDataRollbackProcedure(),
            BasicRollbackProcedure(
                disturbance_type_generator=disturbance_type_generator
            ),
            NoSupportingInfoRollbackProcedure(
                age_generator,
                disturbance_type_generator=disturbance_type_generator,
            ),
            RegenDelayRollbackProcedure(
                age_generator,
                disturbance_type_generator=disturbance_type_generator,
            ),
            ShiftDisturbanceProcedure(
                age_generator,
                prioritize_disturbances,
                disturbance_type_generator=disturbance_type_generator,
            ),
            ShiftEstablishmentProcedure(
                age_generator,
                prioritize_disturbances,
                disturbance_type_generator=disturbance_type_generator,
            ),
        ],
        procedure_info_layer=create_procedure_info_layer(landscape),
    )


def run_case(
    rollback_year,
    prioritize_disturbances,
    age_distribution: list[dict],
    classifier_names: list[str],
    inventory_data: dict,
    disturbance_data: list[dict],
    disturbance_type_generator_config: list[dict],
):
    inventory_cols = (
        ["id"]
        + classifier_names
        + ["inventory_year", "establishment_year", "delay"]
    )
    _inventory_data = {
        "id": 1,
        "inventory_year": inventory_data["inventory_year"],
        "establishment_year": inventory_data["establishment_year"],
        "delay": inventory_data["delay"],
    }
    _inventory_data.update({c: inventory_data[c] for c in classifier_names})

    inventory = CaseRunnerLayer(
        "gcbm_inventory",
        layer_data=np.array([[1]]),
        layer_attributes=pd.DataFrame(
            index=[0],
            columns=inventory_cols,
            data=_inventory_data,
        ),
        classifier_names=classifier_names,
        single_value=True,
    )
    disturbance = CaseRunnerLayer(
        "gcbm_disturbance",
        layer_data=np.array([[1]]),
        layer_attributes=pd.DataFrame(
            columns=[
                "id",
                "year",
                "disturbance_type",
                "is_stand_replacing",
                "is_deforestation",
                "regen_delay",
                "age_after",
            ],
            data=[
                {
                    "id": 1,
                    "year": d["year"],
                    "disturbance_type": d["disturbance_type"],
                    "is_stand_replacing": d["is_stand_replacing"],
                    "is_deforestation": d["is_deforestation"],
                    "regen_delay": d["regen_delay"],
                    "age_after": d["age_after"],
                }
                for d in disturbance_data
            ],
        ),
        single_value=False,
        classifier_names=classifier_names,
    )

    landscape = Landscape(inventory, disturbance)

    manager = get_rollback_manager(
        landscape,
        rollback_year,
        age_class_distribution=age_distribution,
        prioritize_disturbances=prioritize_disturbances,
        single_draw=True,
        disturbance_type_generator_config=disturbance_type_generator_config,
    )

    rollback_output = manager.rollback(landscape)

    rollback_output.inventory.age_data[0]
    rollback_output.inventory.delay_data[0]

    rollback_disturbance_data = list(
        rollback_output.disturbance_data.get_layers()
    )
    rollback_last_pass_disturbance_data = list(
        rollback_output.last_pass_disturbance_data.get_layers()
    )
    rollback_disturbances = [
        o.select_all()
        for o in list(rollback_disturbance_data)
        + list(rollback_last_pass_disturbance_data)
    ]

    if rollback_disturbances:
        out_disturbances_df = pd.concat(rollback_disturbances)
    else:
        out_disturbances_df = None

    rollback_inventory_data = {
        "age": rollback_output.inventory.age_data,
        "delay": rollback_output.inventory.delay_data,
    }

    return (
        pd.DataFrame(
            columns=["age", "delay"],
            data=rollback_inventory_data,
        ),
        pd.DataFrame(
            columns=[
                "year",
                "disturbance_type",
                "is_stand_replacing",
                "is_deforestation",
                "regen_delay",
                "age_after",
            ],
            data=out_disturbances_df,
        ),
    )


def run_cbm(
    rollback_year,
    rollback_inventory,
    rollback_disturbance,
    n_cbm_steps=50,
    merch_volumes=None,
    eco_boundary="Montane Cordillera",
    admin_boundary="British Columbia",
    db_path=None,
):
    import pandas as pd
    from types import SimpleNamespace
    from libcbm.model.cbm import cbm_simulator
    from libcbm.model.cbm.stand_cbm_factory import StandCBMFactory

    if not merch_volumes:
        merch_volumes = [
            {
                "species": "Spruce",
                "age_volume_pairs": [
                    [0, 0],
                    [50, 100],
                    [100, 150],
                    [150, 200],
                ],
            }
        ]
    classifiers = {
        "_id": ["1"],
    }
    merch_volumes = [{"classifier_set": ["1"], "merch_volumes": merch_volumes}]

    cbm_factory = StandCBMFactory(classifiers, merch_volumes, db_path=db_path)

    n_steps = n_cbm_steps
    n_stands = 1

    age = int(rollback_inventory.age.iloc[0])
    delay = int(rollback_inventory.delay.iloc[0])

    last_pass_disturbance_type = str(
        rollback_disturbance.loc[rollback_disturbance.year < rollback_year]
        .sort_values(by="year", ascending=False)
        .disturbance_type.iloc[0]
    )

    inventory = pd.DataFrame(
        index=list(range(0, n_stands)),
        columns=[
            "_id",
            "admin_boundary",
            "eco_boundary",
            "age",
            "area",
            "delay",
            "land_class",
            "afforestation_pre_type",
            "historic_disturbance_type",
            "last_pass_disturbance_type",
        ],
        data=[
            [
                "1",
                admin_boundary,
                eco_boundary,
                age,
                1.0,
                delay,
                "UNFCCC_FL_R_FL",
                None,
                "Wildfire",
                last_pass_disturbance_type,
            ]
        ],
    )

    n_stands = len(inventory.index)

    csets, inv = cbm_factory.prepare_inventory(inventory)
    cbm_dist_events = (
        rollback_disturbance.loc[rollback_disturbance.year >= rollback_year][
            ["year", "disturbance_type"]
        ]
        .set_index("year")["disturbance_type"]
        .to_dict()
    )

    cbm_regen_delays = (
        rollback_disturbance.loc[rollback_disturbance.year >= rollback_year][
            ["year", "regen_delay"]
        ]
        .set_index("year")["regen_delay"]
        .to_dict()
    )

    inverted_dist_type_map = {
        v: k for k, v in cbm_factory.disturbance_types.items()
    }
    with cbm_factory.initialize_cbm() as cbm:

        def disturbance_func(t, cbm_vars):
            year = rollback_year + t - 1
            if year in cbm_dist_events:
                cbm_vars.parameters.disturbance_type[
                    :
                ] = inverted_dist_type_map[cbm_dist_events[year]]
                cbm_vars.state["regeneration_delay"] = np.array(
                    [cbm_regen_delays[year]], dtype=np.int32
                )
            else:
                cbm_vars.parameters.disturbance_type[:] = 0

            return cbm_vars

        (
            cbm_results,
            cbm_reporting_func,
        ) = cbm_simulator.create_in_memory_reporting_func(
            classifier_map=cbm_factory.classifier_names,
            disturbance_type_map=cbm_factory.disturbance_types,
        )

        # tracking the spinup results will make libcbm run considerably slower!
        (
            spinup_results,
            spinup_reporting_func,
        ) = cbm_simulator.create_in_memory_reporting_func()

        cbm_simulator.simulate(
            cbm,
            n_steps=n_steps,
            classifiers=csets,
            inventory=inv,
            pre_dynamics_func=disturbance_func,
            reporting_func=cbm_reporting_func,
            spinup_reporting_func=spinup_reporting_func,
        )

        full_result = SimpleNamespace()
        for k in spinup_results.__dict__.keys():
            spinup_results.__dict__[k].insert(
                0,
                "year",
                range(
                    rollback_year - len(spinup_results.pools.index),
                    rollback_year,
                ),
            )
            cbm_results.__dict__[k].insert(
                0, "year", cbm_results.__dict__[k].timestep + rollback_year
            )
            full_result.__dict__[k] = pd.concat(
                [spinup_results.__dict__[k], cbm_results.__dict__[k]]
            )
        full_result.age_by_year = full_result.state[["year", "age"]].set_index(
            "year"
        )

        full_result.pools["total_bio"] = full_result.pools[
            [
                "SoftwoodMerch",
                "SoftwoodFoliage",
                "SoftwoodOther",
                "SoftwoodCoarseRoots",
                "SoftwoodFineRoots",
                "HardwoodMerch",
                "HardwoodFoliage",
                "HardwoodOther",
                "HardwoodCoarseRoots",
                "HardwoodFineRoots",
            ]
        ].sum(axis=1)
        full_result.pools["total_dom"] = full_result.pools[
            [
                "AboveGroundVeryFastSoil",
                "BelowGroundVeryFastSoil",
                "AboveGroundFastSoil",
                "BelowGroundFastSoil",
                "MediumSoil",
                "AboveGroundSlowSoil",
                "BelowGroundSlowSoil",
                "SoftwoodStemSnag",
                "SoftwoodBranchSnag",
                "HardwoodStemSnag",
                "HardwoodBranchSnag",
            ]
        ].sum(axis=1)
        full_result.pools["total_eco"] = full_result.pools[
            ["total_bio", "total_dom"]
        ].sum(axis=1)
        full_result.pools_by_year = full_result.pools[
            ["year", "total_bio", "total_dom", "total_eco"]
        ].set_index("year")
        return full_result
