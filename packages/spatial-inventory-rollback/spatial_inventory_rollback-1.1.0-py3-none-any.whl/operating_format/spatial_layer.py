import numpy as np
from spatial_inventory_rollback.raster import gdal_helpers
from spatial_inventory_rollback.raster.gdal_helpers import GDALHelperDataset
from spatial_inventory_rollback.raster.raster_bound import RasterBound


def get_bounds(path) -> RasterBound:
    """Get the pixel extent of the raster dataset at path

    Args:
        path (str): path to a raster dataset

    Returns:
        RasterBound: a RasterBound object describing the dataset's pixel extent
    """
    return gdal_helpers.get_raster_dimension(path)


def read_layer(
    path, stack_bounds: RasterBound, bounds: RasterBound = None
) -> GDALHelperDataset:
    """Read data and metadata from the raster dataset at the specified path.

    Args:
        path (str): path to a raster dataset
        bounds (RasterBound): a raster bound object specifying the rectangle
            of pixels to read from the raster
        bounds (RasterBound, optional): a RasterBound object specifying a
            rectangle of pixels to read. If unspecified the entire raster
            extent is read and returned. Defaults to None.

    Raises:
        ValueError: raised if the specified stack_bounds do not match the
            full raster extent.

    Returns:
        object: the return value of
            :py:func:`spatial_inventory_rollback.raster.gdal_helpers.read_dataset`
            for the specified file.

    """
    dataset = gdal_helpers.read_dataset(path=path, bounds=bounds)
    if dataset.raster_bounds != stack_bounds:
        raise ValueError(
            f"Stack size mismatch. File: '{path}' "
            f"expected a {stack_bounds.y_size} rows "
            f"by {stack_bounds.x_size} cols raster."
        )
    return dataset


def create_output_layer(
    output_path: str, template_path: str, data_type=None, nodata=None
):
    """Create an empty geotiff raster using the dimension and projection of
    the raster at the specified template_path.

    Args:
        output_path (str): path at which to create the output geotiff raster.
        template_path (str): path of a raster dataset on which to base the
            dimension and projection of the created raster.
        data_type (object, optional): A numpy dtype used to set the data type
            of the resulting raster dataset. If unspecified, the template
            raster data type is used. Defaults to None.
        nodata (number, optional): a number used to indicate null values in
            the resulting raster dataset. If not specified the nodata value
            in the template raster is used. Defaults to None.
    """
    gdal_helpers.create_empty_raster(
        template_path,
        output_path,
        driver_name="GTiff",
        data_type=data_type,
        nodata=nodata,
        raster_band=1,
        options=gdal_helpers.get_default_geotiff_creation_options(),
    )


def write_output(
    bounds: RasterBound, data: np.ndarray, path: str, flattened: bool = True
):
    """Write the specified array to the specified raster filepath.

    Args:
        bounds (RasterBound): a raster bound object specifying the rectangle
            of pixels to write to the raster
        data (numpy.ndarray): a numpy array to write to the raster
        path (str): the output file path for an existing raster
    """
    if flattened:
        # next line seems backwards, but remember it's (rows, cols)
        out_data = data.reshape((bounds.y_size, bounds.x_size))
    else:
        if data.shape != (bounds.y_size, bounds.x_size):
            raise ValueError(
                f"bounds dimension ({bounds.y_size}, {bounds.x_size}) "
                f"does not match data shape ({data.shape})"
            )
        out_data = data
    gdal_helpers.write_output(
        path=path, data=out_data, x_off=bounds.x_off, y_off=bounds.y_off
    )
