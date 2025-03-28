from typing import Union


class MergeInputLayers:
    def __init__(
        self,
        layer_order: int,
        input_database_path: str,
        study_area_path: str,
        transition_rules_path: str,
        inventory_priority: Union[str, float, int],
        default_layer_source: bool,
    ):
        self._layer_order = layer_order
        self._input_database_path = input_database_path
        self._study_area_path = study_area_path
        self._transition_rules_path = transition_rules_path
        self._inventory_priority = inventory_priority
        self._default_layer_source = default_layer_source

    @property
    def layer_order(self):
        return self._layer_order

    @property
    def input_database_path(self):
        return self._input_database_path

    @property
    def study_area_path(self):
        return self._study_area_path

    @property
    def transition_rules_path(self):
        return self._transition_rules_path

    @property
    def inventory_priority(self):
        return self._inventory_priority

    @property
    def default_layer_source(self):
        return self._default_layer_source
