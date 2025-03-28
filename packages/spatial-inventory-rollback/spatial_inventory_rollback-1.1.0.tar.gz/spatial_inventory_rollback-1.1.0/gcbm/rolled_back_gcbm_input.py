from __future__ import annotations
from spatial_inventory_rollback.gcbm.gcbm_input import GCBMInput


class RolledBackGCBMInput(GCBMInput):
    def __init__(
        self, gcbm_input: GCBMInput, gcbm_input_rolled_back: GCBMInput
    ):
        GCBMInput.__init__(
            self,
            input_database_path=gcbm_input_rolled_back.input_database_path,
            study_area_path=gcbm_input_rolled_back.study_area_path,
            transition_rules_path=gcbm_input_rolled_back.transition_rules_path,
        )
        self.source_gcbm_input = gcbm_input

    def get_classifier_layer_info(self, included: str = "all") -> list[dict]:
        return self.source_gcbm_input.get_classifier_layer_info(included)
