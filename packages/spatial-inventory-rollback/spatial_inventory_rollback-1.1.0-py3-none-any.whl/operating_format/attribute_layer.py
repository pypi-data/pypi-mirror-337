import pandas as pd
import numpy as np
from scipy import sparse
import itertools
from spatial_inventory_rollback.operating_format.layer import Layer
from spatial_inventory_rollback.raster.raster_bound import RasterBound


class AttributeLayerStorage:
    def __init__(self, shape, dtype, nodata, as_sparse=True):
        self._numpy_storage = None
        self._sparse_storage = None

        if as_sparse:
            self._sparse_storage = sparse.lil_matrix(shape, dtype=int)


class AttributeLayer(Layer):
    """A spatial layer with attached attribute table

    Args:
        stack_bounds (RasterBound): the raster bound object describing the
            full extent of the raster in pixels.
        flattened (bool): if set to true the layer_data will be allocated as
            a flattend array, and if false it will be stack_bounds.y_size by
            stack_bounds.x_size. Defaults to True.
        nodata (int): The value that can be interpreted as a null value in
            self.layer_data

    """

    def __init__(
        self,
        stack_bounds,
        flattened=True,
        nodata=-1,
        layer_data=None,
        attribute_data=None,
        name=None,
        path=None,
        unique=False,
        columns=None,
    ):
        self._path = path
        self.name = name
        self._stack_bounds = stack_bounds
        self.nodata = nodata
        self.unique = unique

        # flag to indicate whether the layer data is specified in this
        # constructor
        self.__data_specified = False

        shape = (
            (stack_bounds.y_size * stack_bounds.x_size,)
            if flattened
            else (stack_bounds.y_size, stack_bounds.x_size)
        )

        if layer_data is not None or attribute_data is not None:
            if attribute_data is None or layer_data is None:
                raise ValueError(
                    "both layer_data and data must both be specified"
                )

            if layer_data.shape != shape:
                raise ValueError(
                    "specified data has unexpected shape expected: "
                    f"{shape} got {layer_data.shape}"
                )

            self.__data_specified = True
            self._layer_data = layer_data

            self._data = self.__container(
                tuple(r) for _, r in attribute_data.iterrows()
            )
            self.columns = [str(col) for col in attribute_data.columns]
        else:
            self._layer_data = np.full(
                fill_value=nodata, shape=shape, dtype=int
            )
            self._data = self.__container()
            if columns is None:
                raise ValueError("columns must be specified")
            self.columns = [str(col) for col in columns]

    def __container(self, x=None):
        if self.unique:
            if x:
                return {
                    value: index + 1
                    for index, value in enumerate(dict.fromkeys(x))
                }
            else:
                return {}
        else:
            if x:
                return list(x)
            else:
                return []

    @property
    def path(self) -> str:
        return self._path

    @property
    def bounds(self) -> RasterBound:
        return self._stack_bounds

    @property
    def stack_bounds(self) -> RasterBound:
        return self._stack_bounds

    @property
    def layer_data(self) -> np.ndarray:
        return self._layer_data

    def flatten(self):
        self._layer_data = self._layer_data.flatten()

    def select_data(self, layer_id: int) -> pd.DataFrame:
        if self.__data_specified:
            # the id column is not controlled/defined by this class if the
            # data was specified in the constructor, so cannot select by id
            raise ValueError(
                "select_data method cannot be used on this attribute layer"
            )
        if layer_id < 1 or layer_id > len(self._data):
            raise KeyError("specified layer_id not present in data")
        selected_row = next(itertools.islice(self._data, layer_id - 1, None))
        return pd.DataFrame(
            columns=["id"] + self.columns,
            data=[[layer_id] + list(selected_row)],
        )

    def select_all(self) -> pd.DataFrame:
        data = list(self._data) if self.unique else self._data
        df = pd.DataFrame(columns=self.columns, data=data)
        if not self.__data_specified:
            df.insert(0, "id", list(range(1, len(self._data) + 1)))
        return df

    def set_data(self, indices: np.ndarray, data: tuple) -> None:
        """append a single row of data to this layer

        Args:
            indices (numpy.ndarray): the raster indices to associate with
                this row of data
            data (tuple): a single row of data to associate with the
                specified indices
        Raises:
            ValueError: The specified data was not a single row.
            ValueError: The specified indices point to raster cells that have
                already been assigned data
        """

        layer_value = self.nodata
        if not len(data) == len(self.columns):
            raise ValueError(
                "Expected one value for each of the defined columns: "
                f"{self.columns}"
            )

        if not self.unique:
            layer_value = len(self._data) + 1
            self._data.append(data)
        else:
            layer_value = self._data.get(data)
            if layer_value is None:
                layer_value = len(self._data) + 1
                self._data[data] = layer_value

        if (self.layer_data[indices] != self.nodata).any():
            # make a quick check that we are not re-assigning indices since
            # there is no need to support this at this point, and it would
            # make this implementation more complicated since we would have
            # to potentially clean up orphaned data in the dataframe
            raise ValueError("Attempted to reassign indices")

        self._layer_data[indices] = layer_value
