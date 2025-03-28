import psutil
from spatial_inventory_rollback.raster import raster_chunks
from spatial_inventory_rollback.operating_format import spatial_layer
from spatial_inventory_rollback.operating_format.inventory_layer import (
    InventoryLayer,
    InventoryLayerConfig,
)


def assemble_inventory_layer(
    name: str, inventory_layer_info: dict
) -> InventoryLayer:
    """Create an InventoryLayer object, which stores spatial data by unique
    combinations of classifier and age data

    Args:
        inventory_layer_info (dict): a dictionary describing the
            age layer and classifier layers that compose the inventory layer

        Example::

            assemble_inventory_layer(
                inventory_layer_info={
                    "establishment": {
                        "mode": "Age",
                        "path": "./initial_age_moja.tiff",
                        "nodata": -1,
                    },
                    "inventory_year": {
                        "year": 2015
                    }
                    "inventory_delay": {
                        "path": "./inventory_delay_moja.tiff",
                        "nodata": -1
                    }
                    "classifiers": [
                        {"path": "./Classifier1_moja.tiff",
                        "name": "Classifier1",
                        "nodata": -1,
                        "attributes": {
                        1: "TA",
                        2: "BP",
                        3: "BS",
                        4: "JP",
                        5: "WS",
                        6: "WB",
                        7: "BF",
                        8: "GA"}},
                        {"path": "./Classifier2_moja.tiff",
                        "name": "Classifier2",
                        "nodata": -1,
                        "attributes": {
                        1: "5",
                        2: "6",
                        3: "7",
                        4: "8"}},
                    ]
                })

    Returns:
        InventoryLayer: The initialized inventory layer object
    """
    stack_bounds = spatial_layer.get_bounds(
        inventory_layer_info["establishment"]["path"]
    )

    inventory_bounds = list(
        raster_chunks.get_memory_limited_raster_chunks(
            n_rasters=len(inventory_layer_info["classifiers"]) + 1,
            width=stack_bounds.x_size,
            height=stack_bounds.y_size,
            memory_limit_MB=psutil.virtual_memory().available * 0.25 / 1e6,
            bytes_per_pixel=4,
        )
    )

    config_kwargs = dict(
        establishment_mode=inventory_layer_info["establishment"]["mode"],
        establishment_layer_path=inventory_layer_info["establishment"]["path"],
        establishment_layer_nodata=inventory_layer_info["establishment"][
            "nodata"
        ],
        classifiers=inventory_layer_info["classifiers"],
    )
    if (
        "delay" in inventory_layer_info
        and inventory_layer_info["delay"] is not None
    ):
        config_kwargs.update(
            {
                "inventory_delay_layer_path": inventory_layer_info["delay"][
                    "path"
                ],
                "inventory_delay_layer_nodata": inventory_layer_info["delay"][
                    "nodata"
                ],
            }
        )
    if "year" in inventory_layer_info["inventory_year"]:
        config_kwargs.update(
            {"inventory_year": inventory_layer_info["inventory_year"]["year"]}
        )
    elif "path" in inventory_layer_info["inventory_year"]:
        config_kwargs.update(
            {
                "inventory_year_layer_path": inventory_layer_info[
                    "inventory_year"
                ]["path"]
            }
        )

    inventory_layer_config = InventoryLayerConfig(**config_kwargs)

    inventory = InventoryLayer(
        name=name,
        bounds=stack_bounds,
        stack_bounds=stack_bounds,
        inventory_layer_config=inventory_layer_config,
    )
    if len(inventory_bounds) == 1:
        inventory.load_data()
    else:
        for inventory_bound in inventory_bounds:
            inventory_subset = InventoryLayer(
                name=None,
                bounds=inventory_bound,
                stack_bounds=stack_bounds,
                inventory_layer_config=inventory_layer_config,
            )
            inventory_subset.load_data()
            inventory.update(inventory_subset)
    return inventory
