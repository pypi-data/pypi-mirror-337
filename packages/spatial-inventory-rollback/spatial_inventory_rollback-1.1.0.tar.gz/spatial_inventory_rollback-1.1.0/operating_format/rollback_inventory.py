import numpy as np
from spatial_inventory_rollback.operating_format.landscape import Landscape


class RollbackInventory:
    def __init__(self, landscape: Landscape, rollback_year: int):
        bounds = landscape.stack_bounds
        self.rollback_year = rollback_year
        self._age_data = np.full(
            bounds.x_size * bounds.y_size, self.age_nodata, np.int16
        )
        self._delay_data = np.full(
            bounds.x_size * bounds.y_size, self.delay_nodata, int
        )
        pre_rollback_inventory = landscape.get_layer("gcbm_inventory")
        self._classifier_names = pre_rollback_inventory.classifier_names
        self._classifier_attributes = {}
        # self._classifier_data = {}
        for c in self._classifier_names:
            c_info = pre_rollback_inventory.classifier_info[c]
            self._classifier_attributes[c] = {
                v: int(k) for k, v in c_info["attributes"].items()
            }
            # nodata = int(c_info["nodata"])
            # self._classifier_data[c] = np.full(
            #     bounds.x_size * bounds.y_size, nodata, int
            # )

    def set_value(self, indices: np.ndarray, value: dict):
        self._age_data[indices] = (
            self.rollback_year - value["establishment_year"]
        )
        # for c in self._classifier_names:
        #     attribute_table = self._classifier_attributes[c]
        #     # TODO: support expanded classifiers if
        #     # value[c] is a numpy array and not a scalar value
        #     self._classifier_data[c][indices] = attribute_table[value[c]]
        self._delay_data[indices] = value["delay"]

    @property
    def age_data(self) -> np.ndarray:
        return self._age_data

    @property
    def age_nodata(self) -> int:
        return np.iinfo(np.int16).min

    @property
    def classifier_data(self) -> dict:
        raise NotImplementedError()
        # return self._classifier_data

    @property
    def delay_data(self) -> np.ndarray:
        return self._delay_data

    @property
    def delay_nodata(self) -> int:
        return -1
