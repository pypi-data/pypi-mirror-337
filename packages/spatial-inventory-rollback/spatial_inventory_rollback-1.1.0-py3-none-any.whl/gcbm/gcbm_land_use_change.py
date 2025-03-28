class GCBMLandUseChange:
    def __init__(self, gcbm_input_db: str):
        self.gcbm_input_db = gcbm_input_db
        query_result = gcbm_input_db.query("land_use_change_disturbance")
        query_result = query_result.dropna().reset_index(drop=True)
        query_result["is_forest"] = query_result["is_forest"].astype(bool)
        self.afforestation_types = {
            str(row.disturbance_type_name)
            for row in query_result.loc[query_result.is_forest].itertuples()
        }
        self.deforestation_types = {
            str(row.disturbance_type_name)
            for row in query_result.loc[~query_result.is_forest].itertuples()
        }

    def is_deforestation(self, disturbance_info: dict) -> bool:
        """Reads the disturbance info and determines if it corresponds to a
        deforestation disturbance type

        Args:
            disturbance_info (dict): a dictionary with "disturbance_type" as a
                key. The disturbance type name value specified for the key is
                used to check in the GCBM database if they corresponding
                disturbance type is a deforestation disturbance type.
                Other keys will be ignored.

        Returns:
            bool: True if the disturbance info corresponds to a deforestation
                disturbance, otherwise False.
        """
        return disturbance_info["disturbance_type"] in self.deforestation_types

    def is_afforestation(self, disturbance_info: dict) -> bool:
        """Reads the disturbance info and determines if it corresponds to a
        deforestation disturbance type

        Args:
            disturbance_info (dict): a dictionary with "disturbance_type" as a
                key. The disturbance type name value specified for the key is
                used to check in the GCBM database if they corresponding
                disturbance type is a deforestation disturbance type.
                Other keys will be ignored.

        Returns:
            bool: True if the disturbance info corresponds to a deforestation
                disturbance, otherwise False.
        """
        return disturbance_info["disturbance_type"] in self.afforestation_types
