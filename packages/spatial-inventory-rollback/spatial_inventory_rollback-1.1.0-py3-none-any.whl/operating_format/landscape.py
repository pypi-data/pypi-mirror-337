import os
import numpy as np
import pandas as pd
from typing import Iterator
from spatial_inventory_rollback.operating_format import spatial_layer
from spatial_inventory_rollback.operating_format import numpy_optimization
from spatial_inventory_rollback.operating_format.landscape_work_unit import (
    LandscapeWorkUnit,
)
from spatial_inventory_rollback.operating_format.attribute_layer import (
    AttributeLayer,
)
from spatial_inventory_rollback.operating_format.layer import Layer


class Landscape:
    def __init__(self, *layers):
        self.layers: list[Layer] = []
        self.layers_by_name = {}
        self.stack_bounds = None
        for layer in layers:
            self.add_layer(layer)

    def get_layer(self, layer_name: str) -> Layer:
        """Returns the layer in this landscape that matches the specified
        layer_name. If no layer with that name exists in the landscape, None
        is returned.

        Args:
            layer_name (str): The name of the layer to fetch

        Returns:
            Layer, or None: Returns the layer matching the specified name
                or None.
        """
        if layer_name in self.layers_by_name:
            return self.layers_by_name[layer_name]
        return None

    def get_work_units(self) -> Iterator[LandscapeWorkUnit]:
        """Yields a work unit for each unique inventory record, disturbance
        sequence code combination in the landscape

        Yields:
            LandscapeWorkUnit: yields a LandscapeWorkUnit object for each
                unique disturbance sequence, inventory record combination
        """
        unique_values, inverse = numpy_optimization.unique(
            ar=np.column_stack([x.layer_data for x in self.layers]),
            axis=0,
            return_inverse=True,
        )
        indexed_inverse = numpy_optimization.IndexedWhere(inverse)
        for i, value in enumerate(unique_values):
            all_nodata = True
            layer_data = []
            for i_layer, layer in enumerate(self.layers):
                layer_id = value[i_layer]
                layer_data.append(layer.select_data(layer_id))
                if layer_id != layer.nodata:
                    all_nodata = False
            if all_nodata:
                # don't return a work unit if all layers are nodata
                continue

            yield LandscapeWorkUnit(
                indices=indexed_inverse.where(i),
                layer_data={
                    layer.name: layer_data[i_layer]
                    for i_layer, layer in enumerate(self.layers)
                },
            )

    def create_layer(
        self,
        output_path: str,
        data: np.ndarray,
        flattened: bool = True,
        nodata: int = -1,
    ) -> None:
        """Creates a new layer with the same projection, dimensions, etc. as
        the other layers in the landscape.

        Args:
            output_path (str): the path and filename of the layer to create.
            data (numpy.ndarray): the pixel values to write to the new layer.
            flattened (bool): optionally specifies whether the data is
                flattened (the default) or already in the same dimensions as
                the output layer.
            nodata (int, float): Optionally specifies the no data value in the
                resulting layer.  The default value is -1.
        """
        template = next((layer for layer in self.layers if layer.path), None)
        spatial_layer.create_output_layer(
            output_path, template.path, data_type=data.dtype, nodata=nodata
        )
        spatial_layer.write_output(
            template.stack_bounds, data, output_path, flattened=flattened
        )

    def add_layer(self, layer: Layer) -> None:
        if not layer:
            return

        # make sure no duplicate names have occurred
        if layer.name in self.layers_by_name:
            raise ValueError(f"duplicate layer name '{layer.name}' detected")

        self.layers.append(layer)
        self.layers_by_name[layer.name] = layer

        # assert that all layers have the same bounds
        if not self.stack_bounds:
            self.stack_bounds = layer.stack_bounds
        else:
            if self.stack_bounds != layer.stack_bounds:
                raise ValueError(
                    f"layer stack_bounds mismatch {self.stack_bounds} "
                    f"versus {layer.stack_bounds}"
                )

        # flatten the arrays for easier processing
        layer.flatten()

    def save(self, output_dir: str) -> None:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        unique_values, unique_inverse = numpy_optimization.unique(
            ar=np.column_stack([x.layer_data for x in self.layers]),
            axis=0,
            return_inverse=True,
        )

        landscape_df_cols = list(self.layers_by_name.keys())
        landscape_df = pd.DataFrame(
            data=unique_values, columns=landscape_df_cols
        )
        landscape_df.index.name = "id"
        nodata_landscape_filter = (
            landscape_df[landscape_df_cols[0]]
            == self.layers_by_name[landscape_df_cols[0]].nodata
        )
        for col in landscape_df_cols[1:]:
            nodata_landscape_filter = nodata_landscape_filter & (
                landscape_df[col] == self.layers_by_name[col].nodata
            )

        landscape_nodata = -1
        landscape_nodata_row = landscape_df.loc[nodata_landscape_filter]
        if len(landscape_nodata_row.index) > 0:
            landscape_nodata = int(landscape_nodata_row.index[0])

        self.create_layer(
            os.path.join(output_dir, "landscape.tiff"),
            data=unique_inverse.astype(np.int32),
            nodata=landscape_nodata,
        )
        landscape_df.to_csv(os.path.join(output_dir, "landscape.csv"))
        for layer_name, layer in self.layers_by_name.items():
            self.create_layer(
                os.path.join(output_dir, f"{layer_name}.tiff"),
                data=layer.layer_data.astype(np.int32),
                nodata=layer.nodata,
            )
            layer.select_all().to_csv(
                os.path.join(output_dir, f"{layer_name}.csv"), index=False
            )


def load_landscape(landscape_dir: str) -> Landscape:
    landscape_df = pd.read_csv(
        os.path.join(landscape_dir, "landscape.csv"), index_col="id"
    )
    stack_bounds = spatial_layer.get_bounds(
        os.path.join(landscape_dir, "landscape.tiff")
    )
    layers = []
    for column in landscape_df.columns:
        layer_path = os.path.join(landscape_dir, f"{column}.tiff")
        layer_data_path = os.path.join(landscape_dir, f"{column}.csv")
        layer = spatial_layer.read_layer(layer_path, stack_bounds)
        layers.append(
            AttributeLayer(
                stack_bounds=stack_bounds,
                flattened=True,
                nodata=layer.nodata,
                layer_data=layer.data.flatten(),
                attribute_data=pd.read_csv(layer_data_path),
                name=column,
                path=layer_path,
            )
        )
    return Landscape(*layers)
