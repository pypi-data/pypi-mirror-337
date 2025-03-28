import numpy as np

from spatial_inventory_rollback.operating_format.landscape_work_unit import (
    LandscapeWorkUnit,
)
from spatial_inventory_rollback.procedures.age_generator import AgeGenerator
from spatial_inventory_rollback.procedures.categorical_distribution_index import (  # noqa: E501
    CategoricalDistributionIndex,
)


class DistributionAgeGenerator(AgeGenerator):
    def __init__(
        self,
        age_distributions: CategoricalDistributionIndex,
        single_draw: bool = False,
        *args,
        **kwargs,
    ):
        """Generates initial age values by drawing from a probability-weighted
        distribution.

        Args:
            age_class_distribution (pandas.DataFrame): dataframe with columns
                "age", and "p" and other columns, which if present, specify
                the keys that correpsond to the categorical distribution
                defined in columns "age" and "p". The expectation is that the
                sum of the p column for each unique group of keys
                is 1.0.
            single_draw (bool, optional): If false all indices will be
                assigned an age drawn from the specified distribution.
                If set to true all indices in the work unit will get the
                first value drawn from the specified distribution. Defaults
                to False.
        """
        super().__init__(*args, **kwargs)
        self._single_draw = single_draw
        self._age_distributions = age_distributions

    def assign(
        self,
        work_unit: LandscapeWorkUnit,
        distribution_key: dict = None,
        min_years: int = 0,
    ) -> np.ndarray:
        # Draw as many random ages as needed until the sum is greater than
        # min_years.
        work_unit_size = len(work_unit.indices)
        n_samples = work_unit_size if not self._single_draw else 1
        remainder = np.full(shape=(n_samples, 1), fill_value=True)
        age_draws = None

        while remainder.any():
            age_draw = self._age_distributions.random_draw(
                shape=(n_samples, 1), key=distribution_key
            )

            if age_draws is None:  # First draw.
                age_draws = age_draw
                processed_indices = (age_draw > min_years).nonzero()
            else:  # Subsequent draws.
                remainder_subset = np.full((n_samples, 1), np.nan)
                remainder_subset[remainder] = age_draw[remainder]
                age_draws = np.column_stack((age_draws, remainder_subset))
                processed_indices = (
                    age_draws.sum(axis=1, where=~np.isnan(age_draws))
                    > min_years
                ).nonzero()

            remainder[processed_indices] = False

        return age_draws
