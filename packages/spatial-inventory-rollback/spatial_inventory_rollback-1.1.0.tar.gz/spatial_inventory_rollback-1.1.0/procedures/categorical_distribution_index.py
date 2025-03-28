from __future__ import annotations
import json
from itertools import product
from typing import Union
import pandas as pd
import numpy as np
from spatial_inventory_rollback.procedures.wildcard_trie import Trie
from spatial_inventory_rollback.procedures.categorical_distribution import (
    CategoricalDistribution,
)


WILDCARD = "?"


class CategoricalDistributionIndex:
    def __init__(
        self, distributions: pd.DataFrame, distribution_keys: pd.DataFrame
    ):
        """create an distribution index from a pair of dataframes that
        define multiple distribution and keys for each distribution.


        Args:
            distributions (pd.DataFrame): a dataframe with columns:
                "distribution_id", "value", "p" that defines a set of
                distributions.  The specified distributions will be
                expanded to sequential integer years to fill any gaps
                found in the input.
            distribution_keys (pd.DataFrame): a dataframe with columns:
                ["key0", "key1", ..., "keyN", "distribution_id"] that
                associates an array of keys with a specific distribution
                id in the specified `distributions` parameter.
        """
        self._rng = np.random.default_rng()
        self._key_cols = [
            str(x) for x in distribution_keys.columns if x != "distribution_id"
        ]
        self._trie = Trie(WILDCARD)
        self._distribution_by_id = {}
        for distribution_id in distributions["distribution_id"].unique():
            selected_distribution = distributions.loc[
                distributions["distribution_id"] == distribution_id
            ][["value", "p"]].reset_index(drop=True)

            self._distribution_by_id[
                int(distribution_id)
            ] = CategoricalDistribution(
                selected_distribution, value_col="value"
            )
        for _, row in distribution_keys.iterrows():
            distribution_id = int(row["distribution_id"])
            insertion_key = [str(row[k]) for k in self._key_cols]
            self._trie.insert(
                insertion_key, self._distribution_by_id[distribution_id]
            )

    @property
    def key_cols(self) -> list[str]:
        return self._key_cols.copy()

    def index_of_key_col(self, key_col) -> int:
        return self._key_cols.index(key_col)

    def random_draw(
        self, shape: tuple[int], key: dict[str, str]
    ) -> np.ndarray:
        """Create an array of the specified shape filled with random draws
        from the distribution matching the specified key.

        The specified key must have a defined key-value-pair for every key
        column in this instance's distribution_keys dataframe.  Extra keys are
        permitted, but ignored.

        Args:
            shape (tuple[int]): a tuple of integers specifying the dimensions
                of the returned array
            key (dict[str, str]): keys to fetch a matching age-distribution
        """
        if not self._key_cols:
            if len(self._distribution_by_id) > 1:
                raise ValueError(
                    "no keys, but multiple distributions detected"
                )
            distribution = list(self._distribution_by_id.values())[0]
        else:
            _key = [str(key[k]) for k in self._key_cols]
            distribution: CategoricalDistribution = self._trie.find(_key)[0][
                "value"
            ]

        if not distribution:
            raise ValueError(f"found no distribution matching: {key}")
        return self.random_draw_distribution(shape, distribution)

    def random_draw_distribution(
        self, shape: tuple[int], distribution: CategoricalDistribution
    ) -> np.array:
        return self._rng.choice(
            distribution.value, size=shape, p=distribution.p
        )

    def get_matching_distributions(self, key: dict[str, str]) -> list:
        if not self._key_cols:
            if len(self._distribution_by_id) > 1:
                raise ValueError(
                    "no keys, but multiple distributions detected"
                )
            return [{"value": list(self._distribution_by_id.values())[0]}]
        else:
            matches = []
            _key = [str(key[k]) for k in self._key_cols]
            for match in self._trie.find(
                _key,
                best_match_only=False,
                include_score=True,
                include_match=True,
            ):
                matches.append(match)
            return matches


def expand_distribution_values(items: list) -> list:
    output_values = []
    output_p = []
    if len(items) == 1:
        return [tuple(item) for item in items]
    else:
        items = sorted(items, key=lambda x: x[0])
        for i_row in range(len(items)):
            interval_size = (
                items[i_row + 1][0] - items[i_row][0]
                if i_row != len(items) - 1
                else items[i_row][0] - items[i_row - 1][0]
            )
            if interval_size == 0:
                raise ValueError(
                    f"duplicated values detected: {items[i_row][0]}"
                )
            value_range = list(
                range(
                    int(items[i_row][0]), int(items[i_row][0] + interval_size)
                )
            )
            output_values.extend([value for value in value_range])
            output_p.extend(
                [items[i_row][1] / interval_size] * len(value_range)
            )
        if not np.isclose(sum(output_p), 1.0):
            raise ValueError("distribution values do not sum to 1.0")
        return list(zip(output_values, output_p))


def load_distribution_config(
    distribution: Union[str, list[dict]], expand_distribution=False
) -> CategoricalDistributionIndex:
    """Loads categorical distributions from a list of dictionaries
    representing age distributions or and equivalently formatted json file

    The input distribution contains list of dictionaries with the following
    entries:

        * a single key named "distribution" that contains a list of
          (value, probability) rows values
        * 0 or more key value pairs that identify the corresponding
          distribution. The values are lists, and each combination of the
          key values (the cartesian product) of all value lists defines the
          set of keys to the distribution

    The list may contain zero or one entries that has no keys to
    identify the distribution.  This actas as a "default" distribution if
    it is present, for the case where a distribution is requested but no
    match is found.  If a default distribution is not specifed, a request
    that matches no entry will result in an error.

    Example input::

        [
            {
                "distribution": [
                    [50, 0.5],
                    [60, 0.5],
                ]
            },
            {
                "key0": ["valueA1", "valueA2"],
                "key1": ["valueB"],
                "distribution": [
                    [75, 0.5],
                    [80, 0.5],
                ]
            },
            {
                "key2": ["valueC1", "valueC2"],
                "key0": ["valueA1"]
                "distribution": [
                    [100, 0.5],
                    [120, 0.5],
                ]
            }
        ]

    Example Return Value (based on above example)::

        AgeDistributionIndex(
            pd.DataFrame(
                columns=["distribution_id", "value", "p"],
                data=[
                    [1, 50, 0.5],
                    [1, 60, 0.5],
                    [2, 75, 0.5],
                    [2, 80, 0.5],
                    [3, 100, 0.5],
                    [3, 120, 0.5],
                ]
            ),
            pd.DataFrame(
                columns=["key0", "key1", "key2", "distribution_id"],
                data=[
                    ["?", "?", "?", 1],
                    ["valueA1", "valueB", "?", 2],
                    ["valueA2", "valueB", "?", 2],
                    ["valueA1", "?", "valueC1", 3],
                    ["valueA1", "?", "valueC2", 3]
                ]
            )

    Args:
        path (list, str): path to an age distribution json file

    Returns:
        CategoricalDistributionIndex: an instance of an object which allows
            flexible querying of random age draws by multiple keys including
            wildcards.
    """
    if isinstance(distribution, list):
        config = distribution
    else:
        config: list[dict] = json.load(open(distribution, "r"))
    combined_distributions = pd.DataFrame()
    distribution_keys = pd.DataFrame()
    for i_item, item in enumerate(config):
        distribution_id = int(i_item) + 1
        distribution_items = item["distribution"]
        if expand_distribution:
            distribution_items = expand_distribution_values(distribution_items)

        distribution = pd.DataFrame(
            columns=["distribution_id", "value", "p"],
            data={
                "distribution_id": distribution_id,
                "value": [d[0] for d in distribution_items],
                "p": [float(d[1]) for d in distribution_items],
            },
        )
        combined_distributions = pd.concat(
            [
                combined_distributions,
                distribution,
            ]
        )
        item_key_cols = list(set(item.keys()).difference(["distribution"]))
        for key in item_key_cols:
            item[key] = [str(x) for x in item[key]]
        if item_key_cols:
            item_distribution_keys = pd.DataFrame(
                columns=item_key_cols,
                data=list(product(*[item[k] for k in item_key_cols])),
            )

            item_distribution_keys.insert(
                len(item_key_cols), "distribution_id", distribution_id
            )
        else:
            item_distribution_keys = pd.DataFrame(
                {"distribution_id": [distribution_id]}
            )
        distribution_keys = pd.concat(
            [distribution_keys, item_distribution_keys]
        )
        distribution_keys = distribution_keys.fillna(WILDCARD)
        distribution_keys.reset_index(drop=True)

    if len(distribution_keys.index) > 1:
        key_cols = [
            col
            for col in distribution_keys.columns
            if col != "distribution_id"
        ]
        duplicates = distribution_keys[
            distribution_keys[key_cols].duplicated()
        ]
        if len(duplicates.index) > 0:
            raise ValueError(f"duplicates keys detected: {duplicates}")
    return CategoricalDistributionIndex(
        combined_distributions.reset_index(drop=True),
        distribution_keys.reset_index(drop=True),
    )
