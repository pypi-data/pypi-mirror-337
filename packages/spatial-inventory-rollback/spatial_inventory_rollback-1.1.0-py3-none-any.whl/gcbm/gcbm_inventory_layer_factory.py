from spatial_inventory_rollback.operating_format import inventory_layer_factory
from spatial_inventory_rollback.operating_format.inventory_layer import (
    InventoryLayer,
)
from spatial_inventory_rollback.gcbm.gcbm_input import GCBMInput
from typing import Union


def get_inventory_layer_info(
    gcbm_input: GCBMInput, inventory_year: int, classifiers: str = "all"
) -> dict:
    age_layer_info = gcbm_input.get_age_layer_info()

    inventory_layer_info = {
        "establishment": {
            "mode": "Age",
            "path": age_layer_info["path"],
            "nodata": age_layer_info["nodata"],
        },
        "classifiers": gcbm_input.get_classifier_layer_info(classifiers),
    }

    delay_layer_info = gcbm_input.get_inventory_delay_layer_info()
    if delay_layer_info:
        inventory_layer_info["delay"] = {
            "path": delay_layer_info["path"],
            "nodata": delay_layer_info["nodata"],
        }
    if isinstance(inventory_year, int):
        inventory_layer_info.update(
            {"inventory_year": {"year": inventory_year}}
        )
    else:
        inventory_layer_info.update(
            {"inventory_year": {"path": inventory_year}}
        )
    return inventory_layer_info


def assemble_inventory_layer(
    gcbm_input: GCBMInput,
    inventory_year: Union[int, str],
    layer_name: str = "gcbm_inventory",
    classifiers: Union[str, list] = "all",
) -> InventoryLayer:
    """Assembles an InventoryLayer object from GCBM input

    Args:
        gcbm_input (GCBMInput): an instance of GCBMInput for loading GCBM
            information
        inventory_year (int, str): the inventory year integer, or path to
            integer raster layer. Defines the inventory year (aka. vintage)
            for each inventory record being processed.
        layer_name (str): a label/identifier for this layer, which becomes
            important if multiple inventory layers are used
        classifiers (str, list): one of "all", None, or a list of classifier
            names to include.

    Returns:
        InventoryLayer: an InventoryLayer object
    """
    inventory_layer_info = get_inventory_layer_info(
        gcbm_input, inventory_year, classifiers
    )
    return inventory_layer_factory.assemble_inventory_layer(
        layer_name, inventory_layer_info
    )
