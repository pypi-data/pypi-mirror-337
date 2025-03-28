from __future__ import annotations
from typing import Union
from typing import Callable
from typing import Any
import pandas as pd
import json
import os


def load_json(path: str) -> Union[list, dict]:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def get_layer_filename(layer_name: str, extension: str) -> str:
    """gets the moja layer filename based on the layer name

    Args:
        layer_name (str): the layer's name
        extension (str): the file extension pasted into the filename

    Returns:
        str: the filename for the layer
    """
    if layer_name.endswith("_moja"):
        return f"{layer_name}{extension}"
    return f"{layer_name}_moja{extension}"


class GCBMInput:
    """methods for fetching information from a GCBM input directory
    if keyword args are specified they will override the default paths to gcbm
    inputs:

        - input_database_path: the path to the gcbm input database
        - study_area_path: the path to the study area metadata file
        - transition rules: the path to the transition rules file

    """

    def __init__(
        self,
        input_database_path: str,
        study_area_path: str,
        transition_rules_path: str,
    ):
        self.input_database_path = input_database_path
        self.study_area_path = study_area_path
        self.transition_rules_path = transition_rules_path

    def load_transition_rules(self) -> Union[pd.DataFrame, None]:
        """returns the gcbm transition rules csv file as a pandas.DataFrame

        Returns:
            pandas.DataFrame: the loaded transition rules file
        """
        if self.transition_rules_path:
            return pd.read_csv(self.transition_rules_path)
        else:
            return None

    def __load_study_area(self):
        """loads the gcbm study area json file as a dictionary

        Returns:
            dict: the loaded file
        """
        return load_json(self.study_area_path)

    def __read_layer_metadata(self, layer_name):
        """Reads the json metadata file associated with a GCBM layer

        Args:
            layer_name (str): the layer name as defined in the GCBM study area
                format.

        Returns:
            dict: the contents of the layer metadata file as a dictionary
        """
        layer_metadata_dir = os.path.join(
            os.path.dirname(self.study_area_path)
        )
        layer_metadata_path = os.path.join(
            layer_metadata_dir, get_layer_filename(layer_name, ".json")
        )
        return load_json(layer_metadata_path)

    def get_disturbance_layer_info(
        self,
        property_funcs: Callable[[dict], Any],
    ) -> list[dict]:
        """Returns the GCBM disturbance layer information relevant to the
        rollback tool.

        Args:

            property_funcs (dict): dictionary of functions that append
                properties to the output.  Signature of each func is:
                    f(attribute) -> (value) THe func return value is inserted
                    to the resulting disturbance layer info using the
                    associated dictionary key.

        Returns:

            list: returns dictionaries describing information relevant to
                spatial rollback for GCBM disturbance layers.

                Example::

                    [{
                        "path": "./disturbances_1984_moja.tiff",
                        "nodata": 255,
                        "attributes": "1": {
                            "year": 1984,
                            "disturbance_type": "Wildfire",
                    }, ... ]

                    property_funcs = {
                        "is_stand_replacing": lambda attribute: (
                            attribute["disturbance_type"] == "Wildfire")
                    }

                If transition rules are included it will include the
                transition rule items in each returned dictionary::

                    [{
                        "path": "./disturbances_1984_moja.tiff",
                        "nodata": 255,
                        "attributes": "1": {
                            "year": 1984,
                            "disturbance_type": "Wildfire",
                            "is_stand_replacing": True,
                            "regen_delay": 1,
                            "age_after": 0,
                            "classifier1": None,
                            "classifier2": "a"
                    }, ... ]

        """
        disturbance_layer_info = []
        study_area = self.__load_study_area()
        layer_dir = os.path.join(os.path.dirname(self.study_area_path))

        transition_rules = self.load_transition_rules()
        has_transition_rules = True
        classifier_names = [
            c["name"] for c in self.get_classifier_layer_info()
        ]
        if transition_rules is None:
            has_transition_rules = False
        transition_rule_attribute_cols = []
        if transition_rules is not None:
            transition_rule_attribute_cols = list(transition_rules.columns[1:])
        else:
            transition_rule_attribute_cols = [
                "regen_delay",
                "age_after",
            ] + classifier_names
        default_transition_rule_values = {"regen_delay": 0, "age_after": -1}
        default_transition_rule_values.update(
            {c: "?" for c in classifier_names}
        )
        for layer in study_area["layers"]:
            if "tags" in layer and "disturbance" in layer["tags"]:
                layer_path = os.path.join(
                    os.path.abspath(layer_dir),
                    get_layer_filename(layer["name"], ".tiff"),
                )

                layer_metadata = self.__read_layer_metadata(layer["name"])
                attributes = {}
                layer_attributes = layer_metadata["attributes"]
                for attribute_id, attribute in layer_attributes.items():
                    new_attribute = {
                        "year": attribute["year"],
                        "disturbance_type": attribute["disturbance_type"],
                    }

                    new_attribute.update(
                        {
                            x: default_transition_rule_values[x]
                            for x in transition_rule_attribute_cols
                        }
                    )

                    if has_transition_rules:
                        transition = (
                            attribute["transition"]
                            if "transition" in attribute
                            else None
                        )
                        if transition:
                            tr = transition_rules.loc[
                                transition_rules.id == transition
                            ].drop(columns="id")
                            if tr.shape[0] == 1:
                                for col in transition_rule_attribute_cols:
                                    new_attribute[col] = tr[col].iloc[0]

                    property_func_updates = {
                        name: func(new_attribute)
                        for name, func in property_funcs.items()
                    }
                    new_attribute.update(property_func_updates)
                    attributes[int(attribute_id)] = new_attribute

                disturbance_layer_info.append(
                    {
                        "path": layer_path,
                        "nodata": layer_metadata["nodata"],
                        "last_pass": "last_pass_disturbance" in layer["tags"],
                        "attributes": attributes,
                    }
                )

        return disturbance_layer_info

    def get_age_layer_info(self) -> dict:
        """Returns GCBM initial_age layer information

        Returns:

            dict: a dictionary describing the inventory age layer

            Example::

                {
                    "path": "./initial_age_moja.tiff",
                    "nodata": 255
                }
        """
        layer_dir = os.path.join(os.path.dirname(self.study_area_path))
        layer_path = os.path.join(
            os.path.abspath(layer_dir),
            get_layer_filename("initial_age", ".tiff"),
        )
        layer_metadata = self.__read_layer_metadata("initial_age")
        return {"path": layer_path, "nodata": layer_metadata["nodata"]}

    def get_inventory_delay_layer_info(self):
        """Returns GCBM inventory_delay layer information, if it exists

        Returns:
            dict: a dictionary describing the inventory delay layer.
                If no inventory layer exists, None is returned

                Example::

                    {
                        "path": "./inventory_delay_moja.tiff",
                        "nodata": 255
                    }
        """
        layer_dir = os.path.join(os.path.dirname(self.study_area_path))

        layer_path = os.path.join(
            os.path.abspath(layer_dir),
            get_layer_filename("inventory_delay", ".tiff"),
        )
        if not os.path.exists(layer_path):
            return None
        layer_metadata = self.__read_layer_metadata("inventory_delay")
        return {"path": layer_path, "nodata": layer_metadata["nodata"]}

    @staticmethod
    def _is_other_layer(layer: dict) -> bool:
        if (
            layer["name"] != "initial_age"
            and layer["name"] != "inventory_delay"
        ):
            if "tags" not in layer:
                return True
            else:
                if (
                    "classifier" in layer["tags"]
                    or "disturbance" in layer["tags"]
                ):
                    return False
                return True
        else:
            return False

    def get_other_layer_info(self) -> list[dict]:
        """Gets the layer information for all layers in the study area which
        are not age layer, classifier layers or disturbance layers.

        Returns:
            list: a list of dictionaries describing the other layers
        """
        study_area = self.__load_study_area()
        other_layer_info = []
        layer_dir = os.path.join(os.path.dirname(self.study_area_path))

        for layer in study_area["layers"]:
            layer_name = layer["name"]
            if self._is_other_layer(layer):
                layer_metadata = self.__read_layer_metadata(layer_name)
                if "attributes" in layer_metadata:
                    attributes = {
                        int(k): v
                        for k, v in layer_metadata["attributes"].items()
                    }
                else:
                    attributes = {}

                layer_info = {
                    "path": os.path.join(
                        os.path.abspath(layer_dir),
                        get_layer_filename(layer_name, ".tiff"),
                    ),
                    "name": layer_name,
                    "nodata": layer_metadata["nodata"],
                }
                if attributes:
                    layer_info["attributes"] = attributes

                other_layer_info.append(layer_info)

        return other_layer_info

    def __get_classifier_layers(self) -> list[dict]:
        study_area = self.__load_study_area()
        layer_dir = os.path.join(os.path.dirname(self.study_area_path))
        classifier_layers = []
        for layer in study_area["layers"]:
            if "tags" in layer and "classifier" in layer["tags"]:
                layer_path = os.path.join(
                    os.path.abspath(layer_dir),
                    get_layer_filename(layer["name"], ".tiff"),
                )
                layer_metadata = self.__read_layer_metadata(layer["name"])
                classifier_layers.append(
                    {
                        "path": layer_path,
                        "name": layer["name"],
                        "nodata": layer_metadata["nodata"],
                        "attributes": {
                            int(k): str(v)
                            for k, v in layer_metadata["attributes"].items()
                        },
                    }
                )
        return classifier_layers

    def get_classifier_layer_info(self, included: str = "all") -> list[dict]:
        """Get a list of the metadata for all classifier layers in the gcbm
            input

        Args:
            included (str, list): one of "all", None, or a list of classifier
                names to include.

        Returns:

            list: a list of classifier metadata including the path and items
                drawn from the study area and classifier layer metadata.


            Example::

                [
                    {"path": "./Classifier1_moja.tiff",
                     "name": "Classifier1",
                     "nodata": 100,
                     "attributes": {
                       1: "TA",
                       2: "BP",
                       3: "BS",
                       4: "JP",
                       5: "WS",
                       6: "WB",
                       7: "BF",
                       8: "GA"}},
                    {"path": "./Classifier2_moja.tiff",
                     "name": "Classifier2",
                     "nodata": -1,
                     "attributes": {
                       1: "5",
                       2: "6",
                       3: "7",
                       4: "8"}},
                ]
        """
        if not included:
            return []

        layers = self.__get_classifier_layers()
        if included == "all":
            return layers
        else:
            include_filter = set(included)
            layer_names = set([x["name"] for x in layers])
            # validate include filter, any names specified here that
            # are not in the set of defined classifier names should cause an
            # error.
            undefined_classifiers = include_filter.difference(layer_names)
            if undefined_classifiers:
                raise ValueError(
                    "The following include classifiers are not defined in "
                    f"gcbm layers {undefined_classifiers}"
                )
            else:
                return [x for x in layers if x["name"] in include_filter]
