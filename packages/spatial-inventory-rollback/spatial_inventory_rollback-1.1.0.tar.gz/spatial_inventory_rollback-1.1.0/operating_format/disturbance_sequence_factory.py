from __future__ import annotations
import psutil
from spatial_inventory_rollback.raster import raster_chunks
from spatial_inventory_rollback.operating_format import spatial_layer
from spatial_inventory_rollback.operating_format import disturbance_layer
from spatial_inventory_rollback.operating_format.disturbance_sequence import (
    DisturbanceSequenceLayer,
)
from spatial_inventory_rollback.operating_format import (
    stacked_disturbance_layer as sdl,
)


def assemble_disturbance_sequence_layer(
    name,
    disturbance_layer_info: list[dict],
    attribute_sorters: list[sdl.AttributeSorter],
) -> DisturbanceSequenceLayer:
    """Build disturbance sequence layer based on disturbance layers

    Args:
        disturbance_layer_info (list): a list of dictionaries describing the
            disturbance layers from which to build disturbance sequences

        Example::

            assemble_disturbance_sequence_layer(
                disturbance_layer_info=[
                    {
                        "path": "./disturbances_1984_moja.tiff",
                        "nodata": 255,
                        "attributes": {
                            "1": {
                                "year": 1984,
                                "disturbance_type": "Wildfire",
                                "is_stand_replacing": True }}
                    },
                        "path": "./disturbances_1985_moja.tiff",
                        "nodata": 255,
                        "attributes": {
                            "1": {
                                "year": 1985,
                                "disturbance_type": "Wildfire",
                                "is_stand_replacing": True }}
                    }])

        attribute_sorters (AttributeSorter): a list of AttributeSorters used
            to sort within each disturbance event sequences by their
            disturbance attributes.  The sort is executed in list order::

                order_by(
                    attribute_sorters[0],
                    attribute_sorters[1],
                    ...,
                    attribute_sorters[n]
                )

            If an empty list or None is provided, no sorted will be executed.

    Returns:
        DisturbanceSequenceLayer: spatial layer containing unique disturbance
            sequences
    """
    if len(disturbance_layer_info) < 1:
        return None
    stack_bounds = spatial_layer.get_bounds(disturbance_layer_info[0]["path"])
    disturbance_sequences = DisturbanceSequenceLayer(name, stack_bounds)

    disturbance_chunks = raster_chunks.get_memory_limited_raster_chunks(
        n_rasters=len(disturbance_layer_info),
        width=stack_bounds.x_size,
        height=stack_bounds.y_size,
        memory_limit_MB=psutil.virtual_memory().available * 0.25 / 1e6,
        bytes_per_pixel=4,
    )

    for chunk in disturbance_chunks:
        disturbance_layers = []
        for disturbance_info in disturbance_layer_info:
            layer = disturbance_layer.load_disturbance_layer(
                chunk, stack_bounds, disturbance_info
            )
            disturbance_layers.append(layer)
        stacked_layers = sdl.stack_disturbance_layers(disturbance_layers)
        if attribute_sorters:
            stacked_layers = sdl.sort_sequences(
                stacked_layers, attribute_sorters
            )
        disturbance_sequences.append_stacked_disturbance_layer(stacked_layers)

    return disturbance_sequences
