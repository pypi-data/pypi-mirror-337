import pandas as pd
import numpy as np


class CategoricalDistribution:
    def __init__(
        self,
        distribution_df: pd.DataFrame,
        value_col: str,
        probability_col: str = "p",
    ):
        """Validates a table of value, probability pairs for use with numpy
        random.choice or other categorical-distribution-generating methods

        Args:
            distribution_df (pd.DataFrame): A table containing a value column
                and corresponding proportion column.
            value_col (str): the value column name.
            probability_col (str, optional): _description_. Defaults to "p".

        Raises:

            ValueError: duplicated values were found in the specified value
                column
            ValueError: the sum of values in the probability column do not sum
                to 1.0
        """
        if distribution_df[value_col].duplicated().any():
            raise ValueError("duplicate values detected")
        self._value = distribution_df[value_col].to_numpy()
        self._p = distribution_df[probability_col].to_numpy()

        if not np.isclose(self._p.sum(), 1.0):
            raise ValueError(
                f"sum of proportions {self._p.sum()} not close to 1.0"
            )

    @property
    def value(self) -> np.ndarray:
        return self._value

    @property
    def p(self) -> np.ndarray:
        return self._p
