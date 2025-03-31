from estecopy.db._internal import attributes as _attributes
from estecopy.db._internal.symbol_converter import _SymbolConverter


class _DesignTableEncoder:
    __CATEGORIES_KEY = _attributes.CATEGORIES_KEY

    __ID_COLUMN_NAME = _attributes.ID_COLUMN_NAME
    __MARKED_COLUMN_NAME = _attributes.MARKED_COLUMN_NAME
    __VIRTUAL_COLUMN_NAME = _attributes.VIRTUAL_COLUMN_NAME
    __CATALOGUE_COLUMN_PREFIX = _attributes.CATALOGUE_COLUMN_PREFIX
    __INPUT_COLUMN_PREFIX = _attributes.INPUT_COLUMN_PREFIX
    __OUTPUT_COLUMN_PREFIX = _attributes.OUTPUT_COLUMN_PREFIX

    __METADATA_KEY = _attributes.METADATA_KEY

    __CommonTableAttributes = _attributes._CommonTableAttributes

    __BOUNDS_KEY = "bounds"
    __INPUT_TYPES = ("variable", "constant", "expression")
    __TYPE_KEY = __CommonTableAttributes._TYPE_KEY
    __DEFAULT_VALUE_KEY = __CommonTableAttributes._DEFAULT_VALUE_KEY
    __BASE_KEY = __CommonTableAttributes._BASE_KEY
    __FORMAT_KEY = __CommonTableAttributes._FORMAT_KEY
    __DESCRIPTION_KEY = __CommonTableAttributes._DESCRIPTION_KEY
    __ALL_INPUT_PARAMETER_KEYS = (__DEFAULT_VALUE_KEY, __BASE_KEY, __FORMAT_KEY, __DESCRIPTION_KEY)
    __ALL_OUTPUT_PARAMETER_KEYS = (__FORMAT_KEY, __DESCRIPTION_KEY)

    __GOALS_KEY = "goals"
    __INPUTS_KEY = "input_variables"
    __INPUT_LOWER_BOUND_KEY = "lower_bound"
    __INPUT_UPPER_BOUND_KEY = "upper_bound"
    __OUTPUTS_KEY = "output_variables"

    __CATALOGUES_KEY = "catalogues"
    __CATALOGUE_NAME = "name"
    __CATEGORY_NAME_KEY = "name"
    __CATEGORY_SYMBOL_KEY = "symbol"
    __CATEGORY_LABEL = __CommonTableAttributes._CATEGORY_LABEL

    __OBJECTIVES_KEY = __CommonTableAttributes._OBJECTIVES_KEY

    __CONSTRAINTS_KEY = __CommonTableAttributes._CONSTRAINTS_KEY

    __EXPRESSIONS_KEY = "trans_variables"

    __OUTPUT_COLUMNS_FROM_MF = (__OUTPUTS_KEY, __EXPRESSIONS_KEY, __OBJECTIVES_KEY, __CONSTRAINTS_KEY)

    def __init__(self, raw_data, rows):
        self.__metadata = raw_data[self.__METADATA_KEY]
        self.__goals = self.__metadata[self.__GOALS_KEY]
        self.__rows = rows
        self.__encoded_column_names = []
        self.__encoded_rows = []
        self.__encoded_optional_properties = {}
        self.__symbol_converter = _SymbolConverter()
        self.__encode()

    def __encode(self):
        self.__encode_column_names()
        self.__encode_rows_from_values()
        self.__encode_optional_properties()

    def __encode_column_names(self):
        self.__encoded_column_names.extend((self.__ID_COLUMN_NAME, self.__MARKED_COLUMN_NAME, self.__VIRTUAL_COLUMN_NAME))
        for catalogue in self.__metadata[self.__CATALOGUES_KEY]:
            self.__encoded_column_names.append(self.__CATALOGUE_COLUMN_PREFIX + catalogue[self.__CATALOGUE_NAME])
        for input_var in self.__goals[self.__INPUTS_KEY]:
            self.__encoded_column_names.append(self.__INPUT_COLUMN_PREFIX + input_var)
        for goal_type in self.__OUTPUT_COLUMNS_FROM_MF:
            for variable in self.__goals[goal_type]:
                self.__encoded_column_names.append(self.__OUTPUT_COLUMN_PREFIX + variable)

    def __encode_rows_from_values(self):
        if len(self.__encoded_column_names) == 0:
            raise RuntimeError("No encoded column names were found, cannot build rows")
        for i in range(1, len(self.__rows)):
            self.__encoded_rows.append(list(self.__rows[i]))

    def __encode_optional_properties(self):
        self.__encode_inputs_properties()
        self.__encode_outputs_properties()
        self.__encode_catalogues_properties()

    def __encode_inputs_properties(self):
        for variable in self.__goals[self.__INPUTS_KEY]:
            encoded_input_properties = {}
            input_properties = self.__goals[self.__INPUTS_KEY][variable]
            encoded_input_properties[self.__BOUNDS_KEY] = [input_properties[self.__INPUT_LOWER_BOUND_KEY],
                                                           input_properties[self.__INPUT_UPPER_BOUND_KEY]]
            encoded_input_type = input_properties[self.__TYPE_KEY]
            encoded_input_properties[self.__TYPE_KEY] = self.__INPUT_TYPES[encoded_input_type]

            for parameter in self.__ALL_INPUT_PARAMETER_KEYS:
                encoded_input_properties[parameter] = input_properties[parameter]

            self.__encoded_optional_properties[variable] = encoded_input_properties

    def __encode_outputs_properties(self):
        for goal_type in self.__OUTPUT_COLUMNS_FROM_MF:
            for variable in self.__goals[goal_type]:
                self.__encoded_optional_properties[variable] = {}
                for parameter in self.__ALL_OUTPUT_PARAMETER_KEYS:
                    self.__encoded_optional_properties[variable][parameter] = self.__goals[goal_type][variable][parameter]

    def __encode_catalogues_properties(self):
        for catalogue in self.__metadata[self.__CATALOGUES_KEY]:
            self.__encoded_optional_properties[catalogue[self.__CATALOGUE_NAME]] = self.__extract_catalogue_properties(catalogue[self.__CATEGORIES_KEY])

    def __extract_catalogue_properties(self, categories):
        catalogue_properties = {}
        for category in categories:
            catalogue_properties[category[self.__CATEGORY_NAME_KEY]] = {}
            catalogue_properties[category[self.__CATEGORY_NAME_KEY]][self.__CATEGORY_LABEL] = category[self.__CATEGORY_LABEL]
            catalogue_properties[category[self.__CATEGORY_NAME_KEY]].update(self.__symbol_converter.string_to_dict(category[self.__CATEGORY_SYMBOL_KEY]))
        return catalogue_properties

    def get_encoded_column_names(self):
        return self.__encoded_column_names

    def get_encoded_rows(self):
        return self.__encoded_rows

    def get_encoded_optional_properties(self):
        return self.__encoded_optional_properties
