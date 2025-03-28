class RollbackAppParameters:
    def __init__(
        self,
        output_path: str,
        input_db: str,
        input_layers: str,
        inventory_year: int,
        rollback_year: int,
        rollback_age_distribution: str,
        prioritize_disturbances: bool,
        single_draw: bool,
        establishment_disturbance_type: str,
        establishment_disturbance_type_distribution: str,
        stand_replacing_lookup: str,
        disturbance_type_order: str,
        logging_level: str,
    ):
        self._output_path = output_path
        self._input_db = input_db
        self._input_layers = input_layers
        self._inventory_year = inventory_year
        self._rollback_year = rollback_year
        self._rollback_age_distribution = rollback_age_distribution
        self._prioritize_disturbances = prioritize_disturbances
        self._single_draw = single_draw
        self._establishment_disturbance_type = establishment_disturbance_type
        self._establishment_disturbance_type_distribution = (
            establishment_disturbance_type_distribution
        )
        self._stand_replacing_lookup = stand_replacing_lookup
        self._disturbance_type_order = disturbance_type_order
        self._logging_level = logging_level

    @property
    def output_path(self):
        return self._output_path

    @property
    def input_db(self):
        return self._input_db

    @property
    def input_layers(self):
        return self._input_layers

    @property
    def inventory_year(self):
        return self._inventory_year

    @property
    def rollback_year(self):
        return self._rollback_year

    @property
    def rollback_age_distribution(self):
        return self._rollback_age_distribution

    @property
    def prioritize_disturbances(self):
        return self._prioritize_disturbances

    @property
    def single_draw(self):
        return self._single_draw

    @property
    def establishment_disturbance_type(self):
        return self._establishment_disturbance_type

    @property
    def establishment_disturbance_type_distribution(self):
        return self._establishment_disturbance_type_distribution

    @property
    def stand_replacing_lookup(self):
        return self._stand_replacing_lookup

    @property
    def disturbance_type_order(self):
        return self._disturbance_type_order
