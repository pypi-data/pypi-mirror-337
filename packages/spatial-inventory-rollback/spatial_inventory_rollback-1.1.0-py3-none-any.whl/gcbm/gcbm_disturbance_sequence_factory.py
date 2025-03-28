from __future__ import annotations
from enum import Enum
from spatial_inventory_rollback.gcbm.gcbm_stand_replacing import (
    DefaultStandReplacing,
)
from spatial_inventory_rollback.gcbm.gcbm_stand_replacing import (
    LookupTableStandReplacing,
)
from spatial_inventory_rollback.operating_format import (
    disturbance_sequence_factory,
)
from spatial_inventory_rollback.operating_format.stacked_disturbance_layer import (  # noqa 503
    AttributeSorter,
)
from spatial_inventory_rollback.operating_format.disturbance_sequence import (
    DisturbanceSequenceLayer,
)
from spatial_inventory_rollback.gcbm.gcbm_input_db import GCBMInputDB
from spatial_inventory_rollback.gcbm.gcbm_land_use_change import (
    GCBMLandUseChange,
)
from spatial_inventory_rollback.gcbm.gcbm_input import GCBMInput


class DisturbanceLayerType(Enum):
    All = 0
    SimulationPeriod = 1
    LastPass = 2


def assemble_disturbance_sequence_layer(
    gcbm_input: GCBMInput,
    stand_replacing_lookup: dict[str, bool] = None,
    disturbance_type_order: dict[str, int] = None,
    layer_name: str = "gcbm_disturbance",
    layer_type: DisturbanceLayerType = DisturbanceLayerType.All,
) -> DisturbanceSequenceLayer:
    """Assembles a DisturbanceSequenceLayer object from GCBM input

    Args:
        gcbm_input (GCBMInput): an instance of GCBMInput for loading GCBM
            information
        stand_replacing_lookup (dict, optional): A dictionary of disturbance
            type name (key, str) to a boolean value which indicates when true
            that the disturbance type is stand replacing and if false not stand
            replacing.  If the dictionary is not specified, then the default
            method based on GCBM input is used to determine if disturbance
            types are considered stand replacing. Defaults to None.
        disturbance_type_order (dict, optional): A dictionary of
            {disturbance type name: disturbance type priority} used to sort
            disturbance events within disturbance event sequences. If not
            specified, sequences are formed based on study_area order and not
            sorted.
        layer_name (str): a label/identifier for this layer, which becomes
            important if multiple disturbance layers are used
        layer_type (DisturbanceLayerType): The type of disturbance layers to
            include:
                All (default): everything tagged 'disturbance'
                SimulationPeriod: excludes last pass disturbance layers
                LastPass: last pass disturbance layers only

    Returns:
        DisturbanceSequenceLayer: spatial layer containing unique disturbance
            sequences
    """
    stand_replacing_func = None
    if stand_replacing_lookup:
        lookup_table_stand_replacing = LookupTableStandReplacing(
            stand_replacing_lookup
        )
        stand_replacing_func = lookup_table_stand_replacing.is_stand_replacing
    else:
        default_stand_replacing = DefaultStandReplacing(
            GCBMInputDB(gcbm_input.input_database_path),
            gcbm_input.load_transition_rules(),
        )
        stand_replacing_func = default_stand_replacing.is_stand_replacing

    luc = GCBMLandUseChange(
        gcbm_input_db=GCBMInputDB(gcbm_input.input_database_path)
    )
    all_disturbances = gcbm_input.get_disturbance_layer_info(
        {
            "is_stand_replacing": stand_replacing_func,
            "is_deforestation": luc.is_deforestation,
            "is_afforestation": luc.is_afforestation,
        }
    )

    disturbance_layer_info = (
        all_disturbances
        if layer_type == DisturbanceLayerType.All
        else [layer for layer in all_disturbances if layer["last_pass"]]
        if layer_type == DisturbanceLayerType.LastPass
        else [layer for layer in all_disturbances if not layer["last_pass"]]
    )

    attribute_sorters = [
        AttributeSorter("year", lambda year: int(year))  # sort by year asc
    ]
    if disturbance_type_order:
        # sort by the specified {disturbance type name: priority} pairs
        # if specifed
        attribute_sorters.append(
            AttributeSorter("disturbance_type", disturbance_type_order)
        )
    return disturbance_sequence_factory.assemble_disturbance_sequence_layer(
        layer_name, disturbance_layer_info, attribute_sorters
    )
