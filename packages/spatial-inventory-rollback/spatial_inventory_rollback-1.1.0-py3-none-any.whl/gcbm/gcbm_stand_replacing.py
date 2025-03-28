from __future__ import annotations
import pandas as pd
from spatial_inventory_rollback.gcbm.gcbm_input_db import GCBMInputDB

STAND_REPLACING_PERCENT = 99


class DefaultStandReplacing:
    """Default method to determine if a given disturbance
    is associated with a stand replacing CBM disturbance type.

    The function will first check for a transition rule associated with the
    disturbance, and if present, and the reset_age value of the disturbance
    is set to zero then it will deem the disturbance stand replacing.

    If no zero reset age is found, the function will fetch the disturbance
    matrix info via the disturbance matrices contained in the GCBM database.
    See: :py:class:`spatial_inventory_rollback.gcbm.gcbm_input_db.GCBMInputDB`

    Args:
        gcbm_input_db (GCBMInputDB): object for fetching GCBM disturbance
            related data.
        transition_rules (pandas.DataFrame): a data frame containing GCBM
            transition rules from the standard tiler-generated csv file
            "transitions_rules.csv"
    """

    def __init__(
        self, gcbm_input_db: GCBMInputDB, transition_rules: pd.DataFrame
    ):
        self.gcbm_input_db = gcbm_input_db
        self.transition_rules = transition_rules

        # The set of disturbance types names associated with matrices that
        # have both stand replacing and non-stand replacing matrices defined
        # across spatial units.
        self.mixed_disturbance_matrices = set()

        matrix_df = self.gcbm_input_db.query(
            "stand_replacing_disturbance_matrix"
        )

        self.matrix_stand_replacing_lookup = self._matrix_stand_replacing(
            matrix_df
        )

    def is_stand_replacing(self, disturbance_info: dict) -> bool:
        """Reads the disturbance info and determines if it corresponds to a
        stand replacing disturbance type

        Args:
            disturbance_info (dict): a dictionary with the
                following keys:

                    1. "transition"
                    2. "disturbance_type"

                The transition key is optional, and it's value can also be set
                to None to indicate no transition rule.

                Example::

                    {
                        "transition": 1,
                        "disturbance_type": "Wildfire"
                    }

        Returns:
            bool: True if the disturbance info corresponds to a stand
                replacing disturbance, otherwise False.
        """

        # check if there is a non null transition in the disturbance info
        # parameter
        has_transition = (
            "transition" in disturbance_info
            and disturbance_info["transition"] is not None
        )

        if has_transition:
            transition = disturbance_info["transition"]
            # filter the dataframe for the transition id in the disturbance
            # info
            matching_row = self.transition_rules[
                self.transition_rules.id == transition
            ]

            # Raise an error if the transition rule wasn't found.
            # This must be a problem with the input.
            if len(matching_row.index) != 1:
                raise ValueError(
                    f"did not find transition matching {transition}"
                )

            # get the transition rule age after using iloc
            age_after = matching_row.age_after.iloc[0]
            if age_after >= 0 and age_after <= 1:
                return True
                # the transition rule has a low reset age, so it must be stand
                # replacing!

        dist_type = disturbance_info["disturbance_type"]
        if dist_type in self.mixed_disturbance_matrices:
            raise ValueError(
                f"The specified disturbance type {dist_type} has mixed stand "
                "replacing/non-stand replacing disturbance matrices across "
                "spatial units"
            )

        if dist_type in self.matrix_stand_replacing_lookup:
            return self.matrix_stand_replacing_lookup[dist_type]
        else:
            return False

    def _matrix_stand_replacing(
        self, disturbance_matrices: pd.DataFrame
    ) -> dict[str, bool]:
        """Returns a dictionary lookup based on matrix values indicating
        whether or not each disturbance type is stand replacing

        Thoughts::

            since a disturbance type may correspond to several matrices
            (for difference spatial units/ecozones) there is a possibility
            that some of the matrices might be considered stand replacing
            and others not within a single disturbance type.  If this is
            detected the function will throw an error.

        Args:
            disturbance_matrices (pandas.DataFrame): a dataframe of disturbance
                matrices with columns:

                    - disturbance_type_name - name of the disturbance type
                    - disturbance_matrix_id - id useful for error feedback
                    - spatial_unit_id - id useful for error feedback
                    - pool_name - the name of the biomass pool losing carbon
                    - proportion_lost - the proportion of the biomass pool lost


                Approach::

                    - if all values in the proportion_lost column are close to
                        1 the disturbance type can be assumed to be stand
                        replacing.
                    - if all values in the proportion_lost column are not
                        close to 1 the disturbance type can be assumed to be a
                        partial disturbance.
                    - otherwise throw an error.

        Raises:

            ValueError: Any 2 matrices associated with the disturbance type
                disagree as to whether or not the disturbance type is
                "stand replacing".

        Returns:
            dict: a dictionary containing disturabnce type names (key),
                to bool (value) indicating the named disturbance type is stand
                replacing if true, and otherwise non-stand replacing
        """

        disturbance_matrices["is_stand_replacing"] = (
            disturbance_matrices.proportion_lost
            >= STAND_REPLACING_PERCENT / 100
        )
        grouped_df = (
            disturbance_matrices[
                [
                    "spatial_unit_id",
                    "disturbance_type_name",
                    "is_stand_replacing",
                ]
            ]
            .groupby(["spatial_unit_id", "disturbance_type_name"])
            .all()
            .reset_index()
        )

        grouped_df = (
            grouped_df[["disturbance_type_name", "is_stand_replacing"]]
            .groupby(["disturbance_type_name", "is_stand_replacing"])
            .sum()
            .reset_index()
        )

        counts = grouped_df.disturbance_type_name.value_counts()
        if (counts > 1).any():
            self.mixed_disturbance_matrices = set(counts[counts > 1].index)

        return grouped_df.set_index("disturbance_type_name")[
            "is_stand_replacing"
        ].to_dict()


class LookupTableStandReplacing:
    """Lookup table method used to determine if a given disturbance
    is associated with a stand replacing CBM disturbance type by providing
    an explicit lookup table.

    Args:
        stand_replacing_lookup (dict): a dictionary of disturbance type name
            (key, str), to is_stand_replacing (value, bool) used for the
            return value.
    """

    def __init__(self, stand_replacing_lookup: dict[str, bool]):
        self.stand_replacing_lookup = stand_replacing_lookup

    def is_stand_replacing(self, disturbance_info: dict) -> bool:
        """Reads the disturbance info and determines if it corresponds to a
        stand replacing disturbance type based on the explicit lookup table

        Args:
            disturbance_info (dict): a dictionary containing the key:
                "disturbance_type"

                Example::

                    {
                        "disturbance_type": "Wildfire"
                    }
        Returns:
            bool: True if the disturbance info corresponds to a stand
                replacing disturbance, otherwise False.
        """
        disturbance_type = disturbance_info["disturbance_type"]
        if disturbance_type in self.stand_replacing_lookup:
            return self.stand_replacing_lookup[disturbance_type]
        raise KeyError(
            f"Specified disturbance type '{disturbance_type}' "
            "not present in lookup table."
        )
