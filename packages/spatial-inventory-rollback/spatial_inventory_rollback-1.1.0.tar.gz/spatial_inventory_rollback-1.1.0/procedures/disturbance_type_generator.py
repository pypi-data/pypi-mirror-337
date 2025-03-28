import operator
import numpy as np
from spatial_inventory_rollback.procedures.categorical_distribution_index import (  # noqa: E501
    CategoricalDistributionIndex,
)
from spatial_inventory_rollback.procedures import (
    categorical_distribution_index,
)
from spatial_inventory_rollback.procedures.categorical_distribution import (
    CategoricalDistribution,
)


class DisturbanceTypeGenerator:
    def __init__(
        self, disturbance_type_distributions: CategoricalDistributionIndex
    ):
        self._disturbance_type_distributions = disturbance_type_distributions

    @staticmethod
    def _get_range_score(
        range_tuple: tuple[np.float64, np.float64]
    ) -> np.float64:
        if range_tuple[0] == -np.inf and range_tuple[1] == np.inf:
            return np.inf
        if range_tuple[0] == -np.inf and range_tuple[1] != np.inf:
            return range_tuple[1]
        if range_tuple[0] != -np.inf and range_tuple[1] == np.inf:
            return range_tuple[0]
        else:
            return range_tuple[1] - range_tuple[0]

    def _unpack_range_tuple(
        self, tuple_str: list[str]
    ) -> tuple[np.float64, np.float64]:
        if tuple_str == categorical_distribution_index.WILDCARD:
            return (-np.inf, np.inf)
        tuple_tokens = tuple_str.replace("[", "").replace(")", "").split(",")

        result = (np.float64(tuple_tokens[0]), np.float64(tuple_tokens[1]))
        if result[0] > result[1]:
            raise ValueError(
                f"invalid range tuple: lower bound > upper bound ({result})"
            )
        return result

    def get_random_disturbance_type(self, distribution_key: dict) -> str:
        range_key = distribution_key.copy()
        range_key.update(
            {"disturbance_year_range": categorical_distribution_index.WILDCARD}
        )
        matches = (
            self._disturbance_type_distributions.get_matching_distributions(
                range_key
            )
        )
        if len(matches) == 1:
            single_match = (
                self._disturbance_type_distributions.random_draw_distribution(
                    1, matches[0]["value"]
                )
            )
            return str(single_match[0])
        # now find the match that (among the return matches)
        # * has the highest match score
        # * has the narrowest, but matching year range
        filtered_matches: list[
            tuple[np.float64, int, CategoricalDistribution]
        ] = []
        for match in matches:
            distribution = match["value"]
            score = match["score"]
            key_match = match["match"]
            tuple_str: str = key_match[
                self._disturbance_type_distributions.index_of_key_col(
                    "disturbance_year_range"
                )
            ]
            if tuple_str == categorical_distribution_index.WILDCARD:
                score -= 1
                # deduct one from the classifier match score since
                # no range tuple existing in the config
            range_tuple = self._unpack_range_tuple(tuple_str)
            disturbance_year = int(range_key["disturbance_year"])
            if (
                disturbance_year >= range_tuple[0]
                and disturbance_year < range_tuple[1]
            ):
                filtered_matches.append(
                    (-score, self._get_range_score(range_tuple), distribution)
                )
        distribution = None
        if len(filtered_matches) == 1:
            distribution = filtered_matches[0][2]
        elif filtered_matches:
            distribution = sorted(
                filtered_matches, key=operator.itemgetter(0, 1)
            )[0][2]
        else:
            raise ValueError(
                "found no matching disturbance type distribution for "
                f"key {distribution_key}"
            )
        disturbance_type = (
            self._disturbance_type_distributions.random_draw_distribution(
                1, distribution
            )
        )
        return str(disturbance_type[0])
