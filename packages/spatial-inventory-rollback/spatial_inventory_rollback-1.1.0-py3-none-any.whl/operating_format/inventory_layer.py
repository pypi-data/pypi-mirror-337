from enum import Enum
import numpy as np
import pandas as pd
from typing import Union
from spatial_inventory_rollback.operating_format.layer import Layer
from spatial_inventory_rollback.operating_format import spatial_layer
from spatial_inventory_rollback.operating_format import numpy_optimization
from spatial_inventory_rollback.application import log_helper
from spatial_inventory_rollback.raster.raster_bound import RasterBound

logger = log_helper.get_logger()


class InventoryEstablishmentType(Enum):
    """
    Supported modes for inventory age/establishment variable:

        1. Age: the pixel values on the inventory layer represent the age of
            inventory at the inventory year/vintage. Therefore the
            year of establishment is inventory year minus the age.
        2. Establishment: the pixel value on the inventory layer represents
            the year of establishment.
    """

    Age = 1
    Establishment = 2


def parse_establishment_mode(mode_str: str):
    """converts a from string to a value in InventoryEstablishmentType

    Args:
        mode_str (str): a string value which corresponds to a value in
            :py:class:`InventoryEstablishmentType`

    Raises:
        NotImplementedError: Raised if the specified string does not match a
            value in InventoryEstablishmentType.

    Returns:
        InventoryEstablishmentType: one of the enum values of
            InventoryEstablishmentType.
    """
    if mode_str == "Age":
        return InventoryEstablishmentType.Age
    elif mode_str == "Establishment":
        return InventoryEstablishmentType.Establishment
    else:
        raise NotImplementedError(
            f"specified establishment mode string '{mode_str}' not supported"
        )


class InventoryLayerConfig:
    def __init__(
        self,
        establishment_mode: str,
        establishment_layer_path: str,
        establishment_layer_nodata: int,
        classifiers: list,
        inventory_year: int = None,
        inventory_year_layer_path: str = None,
        inventory_delay_layer_path: str = None,
        inventory_delay_layer_nodata: int = None,
    ):
        """Information for assembling an inventory layer using an age or
        establishment layer, classifiers and inventory year information.

        If establishment mode is set to InventoryEstablishmentType.Age one of
        (but not both of) inventory_year or inventory_year_layer_path must be
        defined to assign the establishment year to each inventory record.

        Args:
            establishment_mode (str): a value
                indicating the meaning of pixel values in the inventory
                layer. (see :py:func:`parse_establishment_mode`)
            establishment_layer_path (str): path to the inventory age or
                establishment raster.
            establishment_layer_nodata (int): nodata value for the raster at
                the establishment_layer_path.
            classifiers (list): a list of metadata describing the
                inventory classifiers.
            inventory_year (int, optional): An inventory year that applies to
                all pixel values in the raster at establishment_layer_path.
                (establishment = inventory_year - age). If the specified
                establishment_mode is Establishment this value should be None.
                Defaults to None.
            inventory_year_layer_path (str, optional): path to a raster which
                defines for each pixel the inventory_year, allowing
                computation of establishment year on a pixel by pixel basis.
                The layer must be of the same spatial extent as the
                establishment layer.  If the specified establishment_mode is
                Establishment this value should be None. Defaults to None.

        Raises:
            ValueError: Raised if the both inventory_year and
                inventory_year_layer_path are specified (not None)
        """
        if (
            inventory_year is not None
            and inventory_year_layer_path is not None
        ):
            raise ValueError(
                "Cannot support both inventory_year, and "
                "inventory_year_layer_path parameters."
            )
        self.establishment_mode = establishment_mode
        self.establishment_layer_path = establishment_layer_path
        self.establishment_layer_nodata = establishment_layer_nodata
        self.classifiers = classifiers
        self.classifier_config = {}
        for c in classifiers:
            classifier_name = c["name"]
            if classifier_name in self.classifier_config:
                raise ValueError(
                    f"duplicate classifier name detected {classifier_name}"
                )
            self.classifier_config[classifier_name] = c
        self.inventory_year = inventory_year
        self.inventory_year_layer_path = inventory_year_layer_path
        self.inventory_delay_layer_path = inventory_delay_layer_path
        self.inventory_delay_layer_nodata = inventory_delay_layer_nodata

    def __eq__(self, value):
        return self.__dict__ == value.__dict__

    def __ne__(self, value):
        return not self.__eq__(value)


class InventoryLayer(Layer):
    def __init__(
        self,
        name: str,
        bounds: RasterBound,
        stack_bounds: RasterBound,
        inventory_layer_config: InventoryLayerConfig,
    ):
        """initialize an InventoryLayer

        Args:
            name (str): name of the layer
            bounds (RasterBound): the bounds of this portion of the inventory
                layer.
            stack_bounds (RasterBound): the full spatial extent
            inventory_layer_config (InventoryLayerConfig): instance of class
                describing the data to load.
        """
        self.name = name
        self._layer_data: np.ndarray = None
        self.inventory_data = None
        self._bounds = bounds
        self._stack_bounds = stack_bounds
        self.nodata = 0
        self.__conf = inventory_layer_config
        self._inventory_data_index = {}

    def _update_index(self):
        inventory_data_split = self.inventory_data.to_dict("split")
        self._inventory_data_index = {
            k: dict(
                zip(
                    inventory_data_split["columns"],
                    inventory_data_split["data"][i],
                )
            )
            for i, k in enumerate(inventory_data_split["index"])
        }

    @property
    def path(self) -> str:
        return self.__conf.establishment_layer_path

    @property
    def bounds(self) -> RasterBound:
        return self._bounds

    @property
    def stack_bounds(self) -> RasterBound:
        return self._stack_bounds

    @property
    def classifier_names(self) -> list:
        return [classifier["name"] for classifier in self.__conf.classifiers]

    @property
    def classifier_info(self) -> dict:
        return self.__conf.classifier_config

    def flatten(self):
        self._layer_data = self._layer_data.flatten()

    @property
    def layer_data(self) -> np.ndarray:
        return self._layer_data

    def select_data(self, layer_id: int) -> dict:
        return self._inventory_data_index[layer_id].copy()

    def select_all(self) -> pd.DataFrame:
        df = self.inventory_data.reset_index()
        df.index.name = "id"
        return df

    def load_data(self) -> None:
        """Load inventory data for the subset defined by this instance's
        bounds property.
        """
        logger.debug(f"load inventory data {self.bounds}")
        inventory_dataset = spatial_layer.read_layer(
            path=self.__conf.establishment_layer_path,
            stack_bounds=self.stack_bounds,
            bounds=self.bounds,
        )

        inventory_establishment = None
        establishment_mode = parse_establishment_mode(
            self.__conf.establishment_mode
        )

        inventory_year = None
        inventory_year_nodata = -1
        if establishment_mode == InventoryEstablishmentType.Age:
            if self.__conf.inventory_year:
                inventory_establishment = self.get_establishment_year(
                    inventory_dataset.data,
                    inventory_dataset.nodata,
                    self.__conf.inventory_year,
                    inventory_year_nodata,
                )
                inventory_year = np.full(
                    shape=(self.bounds.y_size, self.bounds.x_size),
                    fill_value=self.__conf.inventory_year,
                )
                # For all positions where age is no_data set inventory_year to
                # also be no_data.
                inventory_year[
                    inventory_dataset.data == inventory_dataset.nodata
                ] = inventory_year_nodata
            elif self.__conf.inventory_year_layer_path:
                inventory_year_layer_dataset = spatial_layer.read_layer(
                    path=self.__conf.inventory_year_layer_path,
                    stack_bounds=self.stack_bounds,
                    bounds=self.bounds,
                )
                # check if the nodata values are perfectly aligned between the
                # inventory year layer and the inventory layer, if they aren't
                # raise an error
                if (
                    (inventory_dataset.data == inventory_dataset.nodata)
                    != (
                        inventory_year_layer_dataset.data
                        == inventory_year_layer_dataset.nodata
                    )
                ).any():
                    raise ValueError(
                        "inventory year layer and the inventory layer do not "
                        "share identical coordinates for nodata values"
                    )

                inventory_year = inventory_year_layer_dataset.data
                inventory_year_nodata = inventory_year_layer_dataset.nodata
                inventory_establishment = self.get_establishment_year(
                    inventory_dataset.data,
                    inventory_dataset.nodata,
                    inventory_year_layer_dataset.data,
                    inventory_year_nodata,
                )

        classifier_datasets = [
            spatial_layer.read_layer(
                path=classifier["path"],
                stack_bounds=self.stack_bounds,
                bounds=self.bounds,
            )
            for classifier in self.__conf.classifiers
        ]

        if self.__conf.inventory_delay_layer_path:
            delay = spatial_layer.read_layer(
                self.__conf.inventory_delay_layer_path,
                stack_bounds=self.stack_bounds,
                bounds=self.bounds,
            ).data.flatten()
        else:
            # add the "delay inventory parameter" as an empty array
            delay = np.full(
                shape=(self.bounds.y_size * self.bounds.x_size),
                fill_value=0,
                dtype=int,
            )

        arrays = [
            inventory_year.flatten(),
            inventory_establishment.flatten(),
            delay,
        ] + [c.data.flatten() for c in classifier_datasets]

        unique_values, unique_inverse = numpy_optimization.unique(
            ar=np.column_stack(arrays), axis=0, return_inverse=True
        )

        columns = ["inventory_year", "establishment_year", "delay"] + [
            c["name"] for c in self.__conf.classifiers
        ]
        self.inventory_data = pd.DataFrame(columns=columns, data=unique_values)

        self.inventory_data.insert(
            loc=0, column="id", value=self.inventory_data.index + 1
        )

        # find a row that is all nodata (if any)
        nodata_filter = (
            self.inventory_data.establishment_year
            == self.__conf.establishment_layer_nodata
        )
        for c in self.__conf.classifiers:
            nodata_filter = nodata_filter & (
                self.inventory_data[c["name"]] == c["nodata"]
            )

        self._layer_data = (unique_inverse + 1).reshape(
            inventory_dataset.data.shape
        )

        nodata_row = self.inventory_data.loc[nodata_filter, "id"]
        if len(nodata_row.index) > 0:
            nodata = nodata_row.iloc[0]
            # reassign whatever nodata that was assigned above with the class
            # definition of nodata, both on the layer, and in the dataframe
            self._layer_data[self._layer_data == nodata] = self.nodata
            self.inventory_data.loc[nodata_filter, "id"] = self.nodata
            # make the remaining integers consecutive
            self._layer_data[self._layer_data > nodata] -= 1
            self.inventory_data.loc[self.inventory_data.id > nodata, "id"] -= 1

        # re-assign the classifier values to the names rather than the ids
        # from the attribute tables
        for c in self.__conf.classifiers:
            self.inventory_data[c["name"]] = self.inventory_data[
                c["name"]
            ].map(c["attributes"])
        # set any establishment nodata value to nan
        self.inventory_data.loc[
            self.inventory_data["establishment_year"]
            == self.__conf.establishment_layer_nodata,
            "establishment_year",
        ] = np.nan
        # and do the same for nodata values if an inventory_year layer was used
        self.inventory_data.loc[
            self.inventory_data["inventory_year"] == inventory_year_nodata,
            "inventory_year",
        ] = np.nan
        # finally sort the values by id
        self.inventory_data.sort_values(
            by="id", inplace=True, ignore_index=True
        )
        self.inventory_data = self.inventory_data.set_index("id")
        self._update_index()

    def update(self, inventory_layer: "InventoryLayer") -> None:
        """update this layer with values from the stacked inventory data in
        the specified bounds

        Args:
            inventory_layer (InventoryLayer): The layer being used to update
                this inventory layer

        Example state before call to update::

            InventoryLayer(
                layer_data=[
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0]],
                bounds=RasterBound(0, 0, 5, 5),
                stack_bounds=RasterBound(0, 0, 5, 5),
                nodata=0,
                classifiers=[
                    {"name": "Classifier1",
                     "nodata": 0,
                     "attributes": {
                        1: "TA",
                        2: "BP"}},
                    {"name": "Classifier2",
                     "attributes": {
                        1: "5",
                        2: "6",
                        3: "7"}}],
                inventory_data=pd.DataFrame())

            Call 1 to update::

                InventoryLayer(
                    layer_data=[
                        [1, 0],
                        [0, 2]],
                    bounds=RasterBound(0, 0, 2, 2),
                    stack_bounds=RasterBound(0, 0, 5, 5),
                    nodata=0,
                    classifiers=[
                        {"name": "Classifier1",
                         "nodata": 0,
                         "attributes": {
                            1: "TA",
                            2: "BP"}},
                        {"name": "Classifier2",
                         "nodata": 0,
                         "attributes": {
                            1: "5",
                            2: "6",
                            3: "7"}}],
                    inventory_data=pd.DataFrame(
                        index=[1, 2],
                        columns=[
                            "inventory_year", "establishment_year",
                            "Classifier1", "Classifier2"],
                        data=[
                            [2020, 1921, 1, 1],
                            [2020, 1811, 2, 3],
                        ]))

            Call 2 to update::

                InventoryLayer(
                    layer_data=[
                        [1, 1],
                        [0, 2]],
                    bounds=RasterBound(2, 2, 2, 2),
                    stack_bounds=RasterBound(0, 0, 5, 5),
                    nodata=0,
                    classifiers=[
                        {"name": "Classifier1",
                         "nodata": 0,
                         "attributes": {
                            1: "TA",
                            2: "BP"}},
                        {"name": "Classifier2",
                         "nodata": 0,
                         "attributes": {
                            1: "5",
                            2: "6",
                            3: "7"}}],
                    inventory_data=pd.DataFrame(
                        index=[1, 2],
                        columns=[
                            "inventory_year", "establishment_year",
                            "Classifier1", "Classifier2"],
                        data=[
                            [2020, 1811, 2, 3],
                            [2020, 1800, 1, 3],
                        ]))

            After calls 1 and 2::

                InventoryLayer(
                    layer_data=[
                        [1, 0, 0, 0, 0],
                        [0, 2, 0, 0, 0],
                        [0, 0, 2, 2, 0],
                        [0, 0, 0, 3, 0],
                        [0, 0, 0, 0, 0]],
                    bounds=RasterBound(0, 0, 5, 5),
                    stack_bounds=RasterBound(0, 0, 5, 5),
                    nodata=0,
                    classifiers=[
                        {"name": "Classifier1",
                         "nodata": 0,
                         "attributes": {
                            1: "TA",
                            2: "BP"}},
                        {"name": "Classifier2",
                         "nodata": 0,
                         "attributes": {
                            1: "5",
                            2: "6",
                            3: "7"}}],
                    inventory_data=pd.DataFrame(
                        index=[1, 2, 3],
                        columns=[
                            "inventory_year", "establishment_year",
                            "Classifier1", "Classifier2"],
                        data=[
                            [2020, 1921, 1, 1],
                            [2020, 1811, 2, 3],
                            [2020, 1800, 1, 3]
                        ]))
        """
        logger.debug(f"update inventory layer {inventory_layer.bounds}")
        if self._layer_data is None:
            self._layer_data = np.full(
                shape=(self.stack_bounds.y_size, self.stack_bounds.x_size),
                fill_value=self.nodata,
            )

        # Check that the metadata and everything else is compatible first of
        # all.
        if self.stack_bounds != inventory_layer.stack_bounds:
            raise ValueError(
                f"Stack bounds mismatch: {self.stack_bounds} does not match "
                f"{inventory_layer.stack_bounds}."
            )
        if self.__conf != inventory_layer.__conf:
            raise ValueError("InventoryLayer configuration must be identical.")

        columns = ["inventory_year", "establishment_year"] + [
            c["name"] for c in self.__conf.classifiers
        ]
        if self.inventory_data is None:
            self.inventory_data = pd.DataFrame(columns=columns)
            self.inventory_data.index.name = "id"
        self.inventory_data = self.inventory_data.reset_index()
        merge_inventory_data = inventory_layer.inventory_data.reset_index()
        # get the set of records that exist in this inventory layer and in the
        # incoming inventory layer
        existing_records = self.inventory_data.merge(
            merge_inventory_data,
            left_on=columns,
            right_on=columns,
            suffixes=("", "_new"),
            how="inner",
        )

        new_id_map = {
            np.int32(row["id_new"]): np.int32(row["id"])
            for _, row in existing_records.iterrows()
        }
        new_records = None
        if len(self.inventory_data.index) > 0:
            # get the set of records that exist in the incoming inventory
            # layer, but not in this inventory layer (they will be added as
            # new records in the table)
            new_records = merge_inventory_data[
                ~merge_inventory_data.id.isin(existing_records.id_new)
            ]

            # get a map of the ids that need to be re-mapped from the incoming
            # inventory layer id to this instance's inventory layer id
            new_id_base = self.inventory_data.id.max() + 1
            new_id_map.update(
                {
                    np.int32(new_record_id): np.int32(
                        new_record_idx + new_id_base
                    )
                    for new_record_idx, new_record_id in enumerate(
                        new_records.id
                    )
                }
            )

            # update the ids for the incoming records
            new_records = new_records.reset_index(drop=True)
            new_records.id = new_records.id.map(new_id_map)
        else:
            new_records = merge_inventory_data

        # append the incoming records to the existing inventory layer
        self.inventory_data = pd.concat([self.inventory_data, new_records])
        self.inventory_data = self.inventory_data.set_index("id")

        # now update the incoming spatial layer with the re-mapped ids
        new_layer_data = numpy_optimization.map(
            inventory_layer.layer_data, new_id_map
        )

        # assign the chunk to this instance's spatial layer
        y_size = inventory_layer.bounds.y_size
        x_size = inventory_layer.bounds.x_size
        y_offset = inventory_layer.bounds.y_off
        x_offset = inventory_layer.bounds.x_off

        self._layer_data[
            y_offset : y_offset + y_size, x_offset : x_offset + x_size
        ] = new_layer_data
        self._update_index()

    def get_establishment_year(
        self,
        age_layer: np.ndarray,
        age_layer_nodata: int,
        inventory_year: Union[int, np.ndarray],
        inventory_year_nodata: int,
    ) -> np.ndarray:
        """Computes and returns an establishment year based on an age layer
        and inventory year

        The return value has an identical shape as the input age_layer
        parameter.

        establishment_year = inventory_year - age

        Args:
            age_layer (numpy.ndarray): an array of age values
            age_layer_nodata (int): the value indicating null value on the
                age_layer. Locations with value nodata in the input age layer
                will also have the same nodata value in the output layer.
            inventory_year (int, or numpy.ndarray): either a scalar integer or
                a numpy.ndarray of identical shape as the specified age_layer.
            inventory_year_nodata (int): the nodata value corresponding to
                inventory_year array

        Raises:
            ValueError: Raised if pixels with defined age, but undefined
                inventory year are detected.

        Returns:
            numpy.ndarray: the establishment layer values
        """

        establishment_year = age_layer.copy()
        if (
            isinstance(inventory_year, np.ndarray)
            and inventory_year.shape == age_layer.shape
        ):
            if (
                inventory_year[age_layer != age_layer_nodata]
                == inventory_year_nodata
            ).any():
                # check for a condition where the age is defined but
                # the inventory year is not defined, for that case we
                # can't compute an establishment year, and so we can
                # raise an error
                raise ValueError(
                    "pixels with defined age, but undefined inventory year "
                    "detected"
                )
            establishment_year[age_layer != age_layer_nodata] = (
                inventory_year[age_layer != age_layer_nodata]
                - age_layer[age_layer != age_layer_nodata]
            )
        else:
            establishment_year[age_layer != age_layer_nodata] = (
                inventory_year - age_layer[age_layer != age_layer_nodata]
            )
        return establishment_year
