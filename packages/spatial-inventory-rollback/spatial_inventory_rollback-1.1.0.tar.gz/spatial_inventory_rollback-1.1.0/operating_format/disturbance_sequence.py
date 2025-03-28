import numpy as np
import pandas as pd
from spatial_inventory_rollback.operating_format import numpy_optimization
from spatial_inventory_rollback.operating_format.stacked_disturbance_layer import (  # noqa 503
    StackedDisturbanceLayer,
)
from spatial_inventory_rollback.raster.raster_bound import RasterBound
from spatial_inventory_rollback.application import log_helper

logger = log_helper.get_logger()


class DisturbanceSequenceLayer(StackedDisturbanceLayer):
    """Stores a layer of unique disturbance sequences as a single raster
    layer, and also an attached metadata table describing the disturbance
    sequences.

    Args:
        name (str): name identifying layer
        stack_bounds (RasterBound): a RasterBound object which describes
            the full extent in pixels of the landscape being processed
    """

    def __init__(self, name: str, stack_bounds: RasterBound):
        layer_data = np.zeros(
            shape=(stack_bounds.y_size, stack_bounds.x_size), dtype=np.int32
        )
        super().__init__(
            name=name,
            layer_data=layer_data,
            bounds=stack_bounds,
            stack_bounds=stack_bounds,
            nodata=0,
            disturbance_event=None,
            disturbance_sequence=None,
        )

        self.unique_sequences = {}
        self._indexed_data = {}
        self._empty_event = {}
        self._sequence_index = {}

    def _update_index(self) -> None:
        self._empty_event = {
            col: self.disturbance_event[col].head(0).to_numpy()
            for col in self.disturbance_event.columns
        }

        self._indexed_data = {
            col: self.disturbance_event[col].to_numpy()
            for col in self.disturbance_event.columns
        }

        disturbance_sequence_index = (
            self.disturbance_sequence.reset_index().merge(
                self.disturbance_event.reset_index().reset_index()[
                    ["index", "id"]
                ],
                left_on="disturbance_event_id",
                right_on="id",
            )
        )
        self._sequence_index = {}
        for row in disturbance_sequence_index.itertuples():
            if row.sequence_id not in self._sequence_index:
                self._sequence_index[row.sequence_id] = []
            self._sequence_index[row.sequence_id].append(row.index)

    def select_data(self, layer_id: int) -> dict:
        if layer_id not in self._sequence_index:
            return self._empty_event
        return {
            col: self._indexed_data[col][self._sequence_index[layer_id]].copy()
            for col in self.disturbance_event.columns
        }

    def select_all(self) -> pd.DataFrame:
        return (
            self.disturbance_sequence.reset_index()
            .merge(
                self.disturbance_event,
                left_on="disturbance_event_id",
                right_index=True,
            )
            .sort_values(by=["sequence_id", "disturbance_event_id", "year"])
        )

    def append_stacked_disturbance_layer(
        self, stacked_layer: StackedDisturbanceLayer
    ) -> None:
        """Append a stacked layer to this instance's disturbance sequence layer

        The reason this is needed is to allow batched processing of the
        :py:func:`stack_disturbance_layers` function which requires loading of
        potentially many disturbance layers into memory.

        Example:

            With a 5x5 full spatial extent this instance's layer is initially
            all zeros::

                StackedDisturbanceLayer(
                    layer_data=[
                        [0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0]],
                    bounds=RasterBound(0, 0, 5, 5),
                    stack_bounds=RasterBound(0, 0, 5, 5),
                    nodata=0,
                    disturbance_event=None,
                    disturbance_sequence=None)

            Call 1 to this function::

                StackedDisturbanceLayer(
                    layer_data=[[0, 1], [2, 3]],
                    bounds=RasterBound(0, 0, 2, 2),
                    stack_bounds=RasterBound(0, 0, 5, 5),
                    nodata=0,
                    disturbance_event=pd.DataFrame(
                        columns=[
                            "id", "disturbance_type", "year", ...],
                        data=[
                            [1, "Wildfire", 1984, ...],
                            [2, "Wildfire", 1950, ...],
                            [3, "clearcut", 1990, ...]]),
                    disturbance_sequence=pd.DataFrame(
                        columns=["sequence_id", "disturbance_event_id"],
                        data=[
                            [1, 3], # sequence 1 is clearcut 1990
                            [2, 1], # sequence 2 is wildfire 1984
                            [3, 2], # sequence 3 is wildfire 1950
                            [3, 3]] #           and clearcut 1990
                    ))

            Call 2 to this function::

                StackedDisturbanceLayer(
                    layer_data=[[0, 1], [2, 1]],
                    bounds=RasterBound(2, 2, 2, 2),
                    stack_bounds=RasterBound(0, 0, 5, 5),
                    nodata=0,
                    disturbance_event=pd.DataFrame(
                        columns=[
                            "id", "disturbance_type", "year", ...],
                        data=[
                            [1, "Wildfire", 1984, ...],
                            [2, "Wildfire", 1950, ...],
                            [3, "clearcut", 1990, ...]]),
                    disturbance_sequence=pd.DataFrame(
                        columns=["sequence_id", "disturbance_event_id"],
                        data=[
                            [1, 1], # sequence 1 is wildfire 1984
                            [1, 3], #           and clearcut 1990
                            [2, 3]] # sequence 2 is clearcut 1990
                    ))

            Expected value of this instance's layer after calls 1 and 2::

                StackedDisturbanceLayer(
                    layer_data=[
                        [0, 1, 0, 0, 0],
                        [2, 3, 0, 0, 0],
                        [0, 0, 0, 4, 0],
                        [0, 0, 1, 4, 0],
                        [0, 0, 0, 0, 0]],
                    bounds=RasterBound(0, 0, 5, 5),
                    stack_bounds=RasterBound(0, 0, 5, 5),
                    nodata=0,
                    disturbance_event=pd.DataFrame(
                        columns=[
                            "id", "disturbance_type", "year", ...],
                        data=[
                            [1, "Wildfire", 1984, ...],
                            [2, "Wildfire", 1950, ...],
                            [3, "clearcut", 1990, ...]]),
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

            Explanation::

                - The first call writes the pixel value to the
                    RasterBound(0, 0, 2, 2) indices of this layer.
                - The second call reassigns the id (from 1 to 4) for one of
                    the sequences: [(fire, 1984), (clearcut 1990)] and re-uses
                    the id (1) for the other [(clearcut, 1990)]  It assigns
                    these values to RasterBound(2, 2, 2, 2)

        Args:
            stacked_layer (StackedDisturbanceLayer): A stacked disturbance
                layer.  See:
                :py:class:`spatial_inventory_rollback.operating_format.stacked_disturbance_layer.StackedDisturbanceLayer`

        Raises:
            ValueError: the provided argument does not have an identical
                stack_bounds as this instance.
            ValueError: any pair of provided arguments did not have an
                identical disturbance_event table

        """
        logger.debug(
            f"append stacked disturbance layer {stacked_layer.bounds}"
        )
        if stacked_layer.stack_bounds != self.stack_bounds:
            raise ValueError("stack bounds mismatch")
        new_layer_data = None
        if self.disturbance_event is None:
            self.disturbance_event = stacked_layer.disturbance_event.copy()
            self.disturbance_sequence = (
                stacked_layer.disturbance_sequence.copy()
            )
            grouped_sequences = self.disturbance_sequence.groupby(
                "sequence_id"
            )
            for sequence_id, group in grouped_sequences:
                sequence = tuple(group.disturbance_event_id)
                self.unique_sequences[sequence] = sequence_id
            new_layer_data = stacked_layer.layer_data
        elif not self.disturbance_event.equals(
            stacked_layer.disturbance_event
        ):
            raise ValueError("disturbance event tables not equal")
        else:
            next_sequence_id = max(self.unique_sequences.values() or [0]) + 1
            sequence_id_update_map = {}
            # need to merge the disturbance_sequence dataframes
            grouped_sequences = stacked_layer.disturbance_sequence.groupby(
                "sequence_id"
            )
            append_records = {"sequence_id": [], "disturbance_event_id": []}
            new_records = False
            for sequence_id, group in grouped_sequences:
                sequence = tuple(group.disturbance_event_id)
                if sequence in self.unique_sequences:
                    # this means that the disturbance sequence is already
                    # present in the collection, but the sequence_id may need
                    # a change since it's from a different stacked disturbance
                    # layer
                    sequence_id_update_map[np.int32(sequence_id)] = np.int32(
                        self.unique_sequences[sequence]
                    )
                else:
                    new_records = True
                    # this means the disturbance sequence is not present in
                    # the collection, so add it to the local collection with a
                    # new id
                    sequence_id_update_map[np.int32(sequence_id)] = np.int32(
                        next_sequence_id
                    )
                    # append the sequence to the disturbance_sequence
                    # dataframe and local dict
                    self.unique_sequences[sequence] = next_sequence_id
                    for event_id in sequence:
                        append_records["sequence_id"].append(next_sequence_id)
                        append_records["disturbance_event_id"].append(event_id)
                    next_sequence_id = next_sequence_id + 1
            if new_records:
                self.disturbance_sequence = pd.concat(
                    [
                        self.disturbance_sequence,
                        pd.DataFrame(append_records).set_index("sequence_id"),
                    ]
                )

            # now re-map the spatial data and assign it to the local spatial
            # layer
            new_layer_data = numpy_optimization.map(
                stacked_layer.layer_data, sequence_id_update_map
            )

        # assign the chunk to this instance's spatial layer
        y_size = stacked_layer.bounds.y_size
        x_size = stacked_layer.bounds.x_size
        y_offset = stacked_layer.bounds.y_off
        x_offset = stacked_layer.bounds.x_off

        self.layer_data[
            y_offset : y_offset + y_size, x_offset : x_offset + x_size
        ] = new_layer_data
        self._update_index()
