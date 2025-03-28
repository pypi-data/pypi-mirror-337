from __future__ import annotations


class MergeOutputLayers:
    def __init__(
        self,
        merged_db_path: str,
        merged_index_path: str,
        merged_inventory_priority_path: str,
        merged_age_path: str,
        merged_inventory_delay_path: str,
        merged_classifiers: dict,
        merged_disturbances: list[dict],
    ):
        self._merged_db_path = merged_db_path
        self._merged_index_path = merged_index_path
        self._merged_inventory_priority_path = merged_inventory_priority_path
        self._merged_age_path = merged_age_path
        self._moerge_inventory_delay_path = merged_inventory_delay_path
        self._merged_classifiers = merged_classifiers
        self._merged_disturbances = merged_disturbances

    @property
    def merged_db_path(self) -> str:
        """the path to the merged gcbm input database"""
        return self._merged_db_path

    @property
    def merged_index_path(self) -> str:
        """the path to the merged merge index layer"""
        return self._merged_index_path

    @property
    def merged_inventory_priority_path(self) -> str:
        """the path to the merged inventory priority layer"""
        return self._merged_inventory_priority_path

    @property
    def merged_age_path(self) -> str:
        """the path to the merged gcbm age layer"""
        return self._merged_age_path

    @property
    def merged_inventory_delay_path(self) -> str:
        """
        path to the merged gcbm inventory delay layer, this property
        may return null if no >0 delays are found.
        """
        return self._moerge_inventory_delay_path

    @property
    def merged_classifiers(self) -> dict:
        """path and attribute information about the merged classifier layers"""
        return self._merged_classifiers

    @property
    def merged_disturbances(self) -> list[dict]:
        """
        path and attribute information about the merged disturbance
        layers
        """
        return self._merged_disturbances
