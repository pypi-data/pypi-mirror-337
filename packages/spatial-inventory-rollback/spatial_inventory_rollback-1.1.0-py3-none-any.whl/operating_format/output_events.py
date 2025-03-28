from __future__ import annotations
import numpy as np
from copy import deepcopy

OUTPUT_EVENT_COLUMNS = [
    "year",
    "disturbance_type",
    "is_stand_replacing",
    "is_deforestation",
    "age_after",
    "regen_delay",
]

MANDATORY_EVENT_COLUMNS = ["year", "disturbance_type", "is_stand_replacing"]

DEFAULT_VALUES = {"regen_delay": 0, "is_deforestation": False}


class OutputEvents:
    def __init__(self, classifier_names: list[str], rollback_year: int):
        self._rollback_year = rollback_year
        self._columns = OUTPUT_EVENT_COLUMNS.copy()
        self._columns.extend(classifier_names)
        self._classifier_names = classifier_names
        self._default_values = DEFAULT_VALUES.copy()
        self._default_values.update({c: "?" for c in self._classifier_names})
        self._storage_contemporary = {c: [] for c in self._columns}
        self._storage_last_pass = {c: [] for c in self._columns}

    def copy(self) -> "OutputEvents":
        return deepcopy(self)

    def append_events(self, event_table: dict):
        n_rows = 0

        if not event_table:
            raise ValueError("no events defined")
        for m in MANDATORY_EVENT_COLUMNS:
            if m not in event_table:
                raise ValueError(f"mandatory column {m} missing")

        first_col = event_table[MANDATORY_EVENT_COLUMNS[0]]
        if np.isscalar(event_table[MANDATORY_EVENT_COLUMNS[0]]):
            n_rows = 1
            self._append_event_scalar(event_table)
        else:
            n_rows = first_col.size
            self._append_events_np(event_table, n_rows)

    def _append_events_np(self, event_table: dict, n_rows: int):
        for default_col, default_value in self._default_values.items():
            if default_col not in event_table:
                self._storage_extend(
                    default_col, [default_value] * n_rows, event_table["year"]
                )
        if "age_after" not in event_table:
            age_after = [
                0 if is_stand_replacing else -1
                for is_stand_replacing in event_table["is_stand_replacing"]
            ]
            self._storage_extend("age_after", age_after, event_table["year"])
        for col, value in event_table.items():
            if not isinstance(value, np.ndarray):
                raise ValueError("mixed types detected")
            if value.size != n_rows:
                raise ValueError("uneven number of rows detected")
            self._storage_extend(col, value.tolist(), event_table["year"])

    def _append_event_scalar(self, event_table: dict):
        for default_col, default_value in self._default_values.items():
            if default_col not in event_table:
                year = event_table["year"]
                self._storage_append(default_col, default_value, year)
        if "age_after" not in event_table:
            year = event_table["year"]
            age_after = 0 if event_table["is_stand_replacing"] else -1
            self._storage_append("age_after", age_after, year)
        for col, value in event_table.items():
            if not np.isscalar(value):
                raise ValueError("mixed types detected")
            self._storage_append(col, value, event_table["year"])

    def _storage_append(self, col: str, value, year: int):
        if col not in self._storage_contemporary:
            return
        if year >= self._rollback_year:
            self._storage_contemporary[col].append(value)
        else:
            self._storage_last_pass[col].append(value)

    def _storage_extend(self, col: str, values: list, year_col):
        for i, v in enumerate(values):
            self._storage_append(col, v, year_col[i])

    def column_names(self) -> list[str]:
        return list(self._columns)

    @property
    def contemporary_data(self) -> dict[str, list]:
        return self._storage_contemporary

    @property
    def last_pass_data(self) -> dict[str, list]:
        return self._storage_last_pass
