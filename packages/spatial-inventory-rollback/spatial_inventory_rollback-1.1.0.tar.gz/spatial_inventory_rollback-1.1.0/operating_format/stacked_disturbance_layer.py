from __future__ import annotations
from typing import Callable
from typing import Union
import numpy as np
import pandas as pd
from spatial_inventory_rollback.operating_format.layer import Layer
from spatial_inventory_rollback.operating_format import numpy_optimization
from spatial_inventory_rollback.application import log_helper
from spatial_inventory_rollback.raster.raster_bound import RasterBound
from spatial_inventory_rollback.operating_format.disturbance_layer import (
    DisturbanceLayer,
)

logger = log_helper.get_logger()


class StackedDisturbanceLayer(Layer):

    """StackedDisturbanceLayer describes the stacked form of several
        disturbance layers.

    Args:
        name (str): a name/identifier for this layer
        layer_data (numpy.ndarray): the disturbance code for each of the
            disturbances described in the `disturbance_sequence` property
            of this class for each spatial index.
        bounds (RasterBound): Object describing the rectangular subset of
            pixels for which this stack of disturbance layers is defined.
        stack_bounds (RasterBound): Object describing the entire pixel extent
            of the spatial inputs.
        nodata (int): the no data value for the layer data array
        disturbance_event (pandas.DataFrame): data frame containing the
            disturbance event metadata from all layers. The columns are:

            - id - the sequential identifier for the disturbance event in the
                table.
            - layer_path - id for the path of the layer which is the origin for
                the disturbance information in each row.
            - disturbance_type - the string disturbance type name for the row
            - year - the calendar year for the disturbance event for the row
            - is_stand_replacing - boolean flag which indicates if the
                disturbance type is considered stand replacing or not.
        disturbance_sequence (pandas.DataFrame): DataFrame that identifies the
            unique disturbance events sequences.  The columns are:

            - sequence_id - the identifier of each unique sequence (duplicates
                allowed)  This value is referenced by the value of the
                layer_data property of this class
            - disturbance_event_id - the disturbance event associated with the
                sequence_id
    """

    def __init__(
        self,
        name: str,
        layer_data: np.ndarray,
        bounds: RasterBound,
        stack_bounds: RasterBound,
        nodata: int,
        disturbance_event: pd.DataFrame,
        disturbance_sequence: pd.DataFrame,
    ):
        self.name = name
        self._layer_data = layer_data
        self._bounds = bounds
        self._stack_bounds = stack_bounds
        self.nodata = nodata
        self.disturbance_event = disturbance_event
        self.disturbance_sequence = disturbance_sequence

    @property
    def path(self):
        return None

    @property
    def bounds(self):
        return self._bounds

    @property
    def stack_bounds(self):
        return self._stack_bounds

    def flatten(self):
        self._layer_data = self._layer_data.flatten()

    @property
    def layer_data(self) -> np.ndarray:
        return self._layer_data

    def select_data(self, id):
        return None


class AttributeSorter:
    def __init__(
        self,
        attribute_name: str,
        attribute_sort: Union[Callable, dict],
    ):
        self._attribute_name = attribute_name
        self._map_arg = attribute_sort
        self._is_dict = False
        if isinstance(self._map_arg, dict):
            self._is_dict = True

    def sort_attribute(self, layer: StackedDisturbanceLayer) -> dict[int, int]:
        map_series = layer.disturbance_event[self._attribute_name]
        if self._is_dict:
            # validate that all unique values in the series are present in the
            # specified dict
            missing_keys = set(map_series.unique()).difference(
                set(self._map_arg.keys())
            )
            if missing_keys:
                raise ValueError(
                    "the following keys are not present in the specified sort "
                    f"map {missing_keys}"
                )
        sort_value_series = map_series.map(self._map_arg)
        disturbance_event_id_series = layer.disturbance_event.index
        return {
            int(disturbance_event_id_series[idx]): int(
                sort_value_series.iloc[idx]
            )
            for idx in range(0, len(layer.disturbance_event.index))
        }


def sort_sequences(
    layer: StackedDisturbanceLayer, attribute_sorters: list[AttributeSorter]
) -> StackedDisturbanceLayer:
    """Produce a copy of the specified StackedDisturbanceLayer with the internal
    disturbance_sequence dataframe sorted and potentially reduced when
    sorting results in less unique sets of disturbance sequences.

    The ascending order sorting fields used are::

        * disturbance_sequence.sequence_id
        * disturbance_sequence.disturbance_event_id.map(sort_maps[0])
        * disturbance_sequence.disturbance_event_id.map(sort_maps[1])
        * ...
        * disturbance_sequence.disturbance_event_id.map(
            sort_maps[len(sort_maps)-1]
            )

    See: pd.Series.map

    Args:
        sort_maps (list[dict[int, int]]): sequence of maps to apply as
            sorting fields on the
            disturbance_sequence.disturbance_event_id column.

    Returns:
        StackedDisturbanceLayer: the copied and sorted stacked disturbance
            layer
    """

    disturbance_sequence = layer.disturbance_sequence.reset_index()
    sort_frame_data = {"sequence_id": disturbance_sequence["sequence_id"]}

    sort_maps = [a.sort_attribute(layer) for a in attribute_sorters]
    for i_sort_map, sort_map in enumerate(sort_maps):
        # validate the sort maps, confirm that each unique value in
        # disturbance_sequence.disturbance_event_id appears in each
        # sort map
        missing_keys = set(
            disturbance_sequence["disturbance_event_id"].unique()
        ).difference(set(sort_map.keys()))
        if missing_keys:
            raise ValueError(
                "the following keys are not present in the specified sort map "
                f"{missing_keys}"
            )
        sort_frame_data[f"sort_col_{i_sort_map}"] = disturbance_sequence[
            "disturbance_event_id"
        ].map(sort_map)

    sort_frame = pd.DataFrame(sort_frame_data)
    sort_cols = list(sort_frame.columns)
    sort_frame = sort_frame.sort_values(by=sort_cols)
    disturbance_sequence = disturbance_sequence.loc[
        sort_frame.index
    ].reset_index(drop=True)

    # now iterate over the values in disturbance sequence, collecting
    # the unique tuples for each sequence_id
    unique_tuples: dict[tuple, int] = {}
    disturbance_event_id_replacement: dict[int, int] = {}
    output_sequences_id = []
    output_disturbance_event_id = []
    for seq in disturbance_sequence.groupby("sequence_id"):
        sequence_id = int(seq[0])
        disturbance_event_id_tuple = tuple(
            [int(x) for x in seq[1]["disturbance_event_id"]]
        )
        if disturbance_event_id_tuple in unique_tuples:
            disturbance_event_id_replacement[sequence_id] = unique_tuples[
                disturbance_event_id_tuple
            ]
        else:
            unique_tuples[disturbance_event_id_tuple] = sequence_id
            output_sequences_id.extend(
                [sequence_id] * len(disturbance_event_id_tuple)
            )
            output_disturbance_event_id.extend(disturbance_event_id_tuple)
    output_disturbance_sequence = pd.DataFrame(
        columns=["sequence_id", "disturbance_event_id"],
        data={
            "sequence_id": output_sequences_id,
            "disturbance_event_id": output_disturbance_event_id,
        },
    )

    output_layer_data = numpy_optimization.map(
        layer.layer_data, disturbance_event_id_replacement
    )

    return StackedDisturbanceLayer(
        name=layer.name,
        layer_data=output_layer_data,
        bounds=layer.bounds,
        stack_bounds=layer.stack_bounds,
        nodata=layer.nodata,
        disturbance_event=layer.disturbance_event,
        disturbance_sequence=output_disturbance_sequence.set_index(
            "sequence_id"
        ),
    )


def stack_disturbance_layers(
    disturbance_layers: list[DisturbanceLayer],
) -> StackedDisturbanceLayer:
    """Given a list of disturbance layers produce a single merged layer
    with a code for each unique disturbance sequence found in the disturbance
    layers.

    The layer data value of each disturbance layer in the sequence must be of
    the same dimension, and they are assumed to be aligned spatially, meaning
    that a given pixel location corresponds to an identical spatial coordinate
    for all layers in the input sequence.

    Each element in the sequence must have identical bounds and stack_bounds
    properties and this function will enforce this by raising a ValueError if
    any 2 elements have differing values for either of these properties.

    Example:

        Input::

            disturbance_layers = [
                DisturbanceLayer(
                    layer_data=np.array([255, 255, 1, 2, 1, 1]),
                    path="./wildfire.tiff",
                    bounds=RasterBound(0, 0, 2, 3),
                    stack_bounds=RasterBound(0, 0, 100, 100),
                    nodata=255,
                    attributes={
                        1: {
                            "year": 1984,
                            "disturbance_type": "Wildfire",
                            "is_stand_replacing": True
                        },
                        2: {
                            "year": 1950,
                            "disturbance_type": "Wildfire",
                            "is_stand_replacing": True
                        }}),
                DisturbanceLayer(
                    layer_data=np.array([-1, 1, -1, 1, -1, 1]),
                    path="./clearcuts.tiff",
                    bounds=RasterBound(0, 0, 2, 3),
                    stack_bounds=RasterBound(0, 0, 100, 100),
                    nodata=-1,
                    attributes={
                        "1": {
                            "year": 1990,
                            "disturbance_type": "clearcut",
                            "is_stand_replacing": True
                        }})]

        Expected Output::

            StackedDisturbanceLayer(
                layer_data=np.array([0, 1, 2, 3, 2, 4]),
                bounds=RasterBound(0, 0, 2, 3),
                stack_bounds=RasterBound(0, 0, 100, 100),
                nodata=0,
                disturbance_event=pd.DataFrame(
                    columns=[
                        "id", "layer_path", "disturbance_type",
                        "year", "is_stand_replacing"],
                    data=[
                        [1, "./wildfire.tiff", "Wildfire", 1984, True],
                        [2, "./wildfire.tiff", "Wildfire", 1950, True],
                        [3, "./clearcut.tiff", "clearcut", 1990, True]]),
                disturbance_sequence=pd.DataFrame(
                    columns=["sequence_id", "disturbance_event_id"],
                    data=[
                        [1, 3], # sequence 1 is clearcut 1990
                        [2, 1], # sequence 2 is wildfire 1984
                        [3, 2], # sequence 3 is wildfire 1950
                        [3, 3], #           and clearcut 1990
                        [4, 1], # sequence 4 is wildfire 1984
                        [4, 3]] #           and clearcut 1990
                ))

    Args:
        disturbance_layers (list): a list of disturbance layers. See:
            :py:class:`spatial_inventory_rollback.operating_format.disturbance_layer.DisturbanceLayer`

    Raises:
        ValueError: any 2 of the provided stacked disturbance layers in the
            input sequence have differing bounds or raster_bounds properties.

    Returns:
        StackedDisturbanceLayer: an object with the stacked form of the
            provided disturbance layers. See:
            :py:class:`StackedDisturbanceLayer`
    """

    if not disturbance_layers or len(disturbance_layers) == 0:
        return None
    logger.debug(f"stack {len(disturbance_layers)} disturbance layers")
    layer_data = None
    stack_bounds = None
    bounds = None
    attribute_cols = set()
    # validate the stack_bounds and bounds
    for layer in disturbance_layers:
        for attribute in layer.attributes.values():
            attribute_cols.update(attribute.keys())

        if stack_bounds is None:
            stack_bounds = layer.stack_bounds
            bounds = layer.bounds
        else:
            if stack_bounds != layer.stack_bounds or bounds != layer.bounds:
                raise ValueError("bounds mismatch")

    disturbance_event_cols = ["id", "path"] + list(attribute_cols)

    # find the unique cases in the spatial data
    stacked_layers = np.column_stack(
        [layer.layer_data.flatten() for layer in disturbance_layers]
    )
    unique_cases, unique_case_inverse = numpy_optimization.unique(
        ar=stacked_layers, axis=0, return_inverse=True
    )

    disturbance_event_data = {col: [] for col in disturbance_event_cols}
    normalized_attribute_ids = [{} for layer in disturbance_layers]
    normalized_attribute_id = 1
    for i_layer, layer in enumerate(disturbance_layers):
        for attribute_id, attribute in layer.attributes.items():
            normalized_attribute_ids[i_layer][
                attribute_id
            ] = normalized_attribute_id

            disturbance_event_data["id"].append(normalized_attribute_id)
            disturbance_event_data["path"].append(layer.path)
            for attribute_col in attribute_cols:
                disturbance_event_data[attribute_col].append(
                    attribute[attribute_col]
                )
            normalized_attribute_id = normalized_attribute_id + 1
    disturbance_event = pd.DataFrame(disturbance_event_data)

    disturbance_sequence_columns = ["sequence_id", "disturbance_event_id"]
    disturbance_sequence_data = {"sequence_id": [], "disturbance_event_id": []}

    sequence_ids = []
    sequence_id = 1
    for _, case in enumerate(unique_cases):
        non_nodata = False
        for layer_idx, attribute_id in enumerate(case):
            layer = disturbance_layers[layer_idx]
            if attribute_id == layer.nodata:
                continue
            else:
                non_nodata = True
                disturbance_sequence_data["sequence_id"].append(sequence_id)
                disturbance_sequence_data["disturbance_event_id"].append(
                    normalized_attribute_ids[layer_idx][attribute_id]
                )
        if non_nodata:
            sequence_ids.append(sequence_id)
            sequence_id = sequence_id + 1
        else:
            sequence_ids.append(0)

    layer_data = np.array(sequence_ids)[unique_case_inverse]

    disturbance_sequence = pd.DataFrame(
        columns=disturbance_sequence_columns, data=disturbance_sequence_data
    )

    return StackedDisturbanceLayer(
        name=None,
        layer_data=layer_data.reshape((bounds.y_size, bounds.x_size)),
        bounds=bounds,
        stack_bounds=stack_bounds,
        nodata=0,
        disturbance_event=disturbance_event.set_index("id"),
        disturbance_sequence=disturbance_sequence.set_index("sequence_id"),
    )
