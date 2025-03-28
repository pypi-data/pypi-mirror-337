from __future__ import annotations
import numpy as np
from spatial_inventory_rollback.operating_format.layer import Layer
from spatial_inventory_rollback.operating_format import spatial_layer
from spatial_inventory_rollback.application import log_helper
from spatial_inventory_rollback.raster.raster_bound import RasterBound

logger = log_helper.get_logger()


class DisturbanceLayer(Layer):
    """Stores items describing a disturbance layer and the layer's data

    Args:
        layer_data (numpy.ndarray): An array of the layer data. The array's
            dimension should be either 2 dimensional matching the bounds
            dimension or the flattened 1 dimensional version of the 2
            dimensional array (see: numpy.flatten)
        path (str): the path of the raster from which the data was drawn
        bounds (RasterBound): a raster bound object describing the rectangluar
            subset in pixels of the raster that layer_data was drawn from
        stack_bounds (RasterBound): the raster bound object describing the
            full extent of the raster in pixels.
        nodata (int): the no data value for the raster
        attributes (dict): a dictionary describing the values in the layer_data

    Example::

        DisturbanceLayer(
            layer_data=numpy.array([255, 255, 1, 255]),
            path="./disturbances_1984_moja.tiff",
            bounds=RasterBound(0,0,2,2),
            stack_bounds=RasterBound(0,0,100,100),
            nodata=255,
            attributes={
                "1": {
                    "year": 1984,
                    "disturbance_type": "Wildfire",
                    "is_stand_replacing": True }})

    """

    def __init__(
        self,
        layer_data: np.ndarray,
        path: str,
        bounds: RasterBound,
        stack_bounds: RasterBound,
        nodata: int,
        attributes: dict[str, dict],
    ):
        self._layer_data = layer_data
        self._path = path
        self._bounds = bounds
        self._stack_bounds = stack_bounds
        self.nodata = nodata
        self.attributes = attributes

    @property
    def path(self):
        return self._path

    @property
    def bounds(self):
        return self._bounds

    @property
    def stack_bounds(self):
        return self._stack_bounds

    @property
    def layer_data(self) -> np.ndarray:
        return self._layer_data

    def flatten(self):
        self._layer_data = self._layer_data.flatten()


def load_disturbance_layer(
    bounds: RasterBound, stack_bounds: RasterBound, config: dict
) -> DisturbanceLayer:
    """Loads disturbance layer data for the specified bounds

    Args:
        bounds (RasterBound): a raster bound object specifying the rectangle
            of pixels to read from the raster
        stack_bounds (RasterBound): a raster bound object for validating the
            expected dimension of the raster dataset.
        config (dict): a dictionary describing the disturbance layer

    Example:

        call::

            load_disturbance_layer(
                bounds=RasterBound(0,0,2,2),
                stack_bounds=RasterBound(0,0,100,100),
                config={
                    "path": "./disturbances_1984_moja.tiff",
                    "nodata": 255,
                    "attributes": {
                        "1": {
                            "year": 1984,
                            "disturbance_type": "Wildfire",
                            "is_stand_replacing": True
                        }
                    }
                })

        format of return value::

            DisturbanceLayer(
                layer_data=numpy.array([255, 255, 1, 255]),
                path="./disturbances_1984_moja.tiff",
                bounds=RasterBound(0,0,2,2),
                stack_bounds=RasterBound(0,0,100,100),
                nodata=255,
                attributes={
                    1: {
                        "year": 1984,
                        "disturbance_type": "Wildfire",
                        "is_stand_replacing": True }})

    Raises:
        ValueError: raised if the data shape is 2 dimensional and
            does not match the bounds shape.
        ValueError: raised if the data shape is 1 dimensional and
            layer_data.shape[0] is not equal to (bounds.x_size * bounds.y_size)

    Returns:
        DisturbanceLayer: a DisturbanceLayer object describing a portion of
            the disturbance layer.
    """
    logger.debug(f"load disturbance layer {bounds}")
    layer_data = spatial_layer.read_layer(config["path"], stack_bounds, bounds)

    # convert attribute ids to integers
    attributes = {
        int(attribute_id): attribute
        for attribute_id, attribute in config["attributes"].items()
    }

    expected_size = bounds.x_size * bounds.y_size
    if layer_data.data.size != expected_size:
        raise ValueError(
            f"size mismatch: expected {expected_size}, and resulting raster "
            f"array is {layer_data.data.size}"
        )
    return DisturbanceLayer(
        layer_data=layer_data.data,
        path=config["path"],
        bounds=bounds,
        stack_bounds=stack_bounds,
        nodata=layer_data.nodata,
        attributes=attributes,
    )
