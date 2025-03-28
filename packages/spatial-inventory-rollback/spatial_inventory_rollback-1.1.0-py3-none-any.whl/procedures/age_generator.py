import numpy as np
from spatial_inventory_rollback.operating_format.landscape_work_unit import (
    LandscapeWorkUnit,
)


class AgeGenerator:
    def __init__(self, *args, **kwargs):
        """Interface for classes that generate ages for a work unit when no
        other supporting information is present.
        """
        pass

    def assign(
        self,
        work_unit: LandscapeWorkUnit,
        distribution_key: dict = None,
        min_years: int = 0,
    ) -> np.ndarray:
        """Assigns an age to the pixels in a work unit according to the
        specific implementation of the AgeGenerator: distribution, fixed
        value, etc.

        Args:
            work_unit (LandscapeWorkUnit): the work unit to generate age values
                for.
            distribution_key (dict): keys corresponding to a particular
                distribution
            min_years: the minimum number of years the draws should cover -
                multiple draws will be made until the sum of the drawn ages
                is greater than the min_years value.

        Returns:
            numpy array of a single age or per-pixel age values.
        """
        raise NotImplementedError()
