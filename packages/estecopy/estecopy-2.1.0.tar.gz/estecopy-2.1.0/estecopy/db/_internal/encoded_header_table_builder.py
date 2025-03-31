import numbers as _numbers
import re as _re
from estecopy._internal import _db
from estecopy._utils import arg_parse as _arg_parse
from estecopy.db._internal import attributes as _attributes
from estecopy.db._internal.symbol_converter import _SymbolConverter
from estecopy.db._internal.table_data_checker import __TableDataChecker


class _EncodedHeaderTableBuilder(__TableDataChecker):
    __INPUTS_KEY = _attributes.INPUTS_KEY
    __OUTPUTS_KEY = _attributes.OUTPUTS_KEY
    __CATEGORIES_KEY = _attributes.CATEGORIES_KEY
    __DATA_KEY = _attributes.DATA_KEY
    __MARKED_KEY = _attributes.MARKED_KEY

    __ID_KEY = _attributes.ID_KEY
    __VIRTUAL_KEY = _attributes.VIRTUAL_KEY

    __ID_COLUMN_NAME = _attributes.ID_COLUMN_NAME
    __MARKED_COLUMN_NAME = _attributes.MARKED_COLUMN_NAME
    __VIRTUAL_COLUMN_NAME = _attributes.VIRTUAL_COLUMN_NAME
    __CATALOGUE_COLUMN_PREFIX = _attributes.CATALOGUE_COLUMN_PREFIX
    __INPUT_COLUMN_PREFIX = _attributes.INPUT_COLUMN_PREFIX
    __OUTPUT_COLUMN_PREFIX = _attributes.OUTPUT_COLUMN_PREFIX

    __CommonTableAttributes = _attributes._CommonTableAttributes

    __BOUNDS_KEY = "bounds"
    __VALID_TYPES = set(("constant", "variable"))
    __TYPE_KEY = __CommonTableAttributes._TYPE_KEY
    __DEFAULT_VALUE_KEY = __CommonTableAttributes._DEFAULT_VALUE_KEY
    __BASE_KEY = __CommonTableAttributes._BASE_KEY
    __FORMAT_KEY = __CommonTableAttributes._FORMAT_KEY
    __DESCRIPTION_KEY = __CommonTableAttributes._DESCRIPTION_KEY
    __ALL_PARAMETER_KEYS = (__BOUNDS_KEY, __TYPE_KEY, __DEFAULT_VALUE_KEY, __BASE_KEY, __FORMAT_KEY, __DESCRIPTION_KEY)

    __CATEGORY_NAMES_KEY = "names"
    __CATEGORY_LABELS_KEY = "labels"
    __CATEGORY_SYMBOLS_KEY = "symbols"
    __EVERY_CATEGORY_KEY = "every_category"
    __CATEGORY_LABEL = __CommonTableAttributes._CATEGORY_LABEL
    __CATEGORY_SYMBOL_SHAPE = __CommonTableAttributes._CATEGORY_SYMBOL_SHAPE
    __CATEGORY_SYMBOL_SIZE = __CommonTableAttributes._CATEGORY_SYMBOL_SIZE
    __CATEGORY_SYMBOL_COLOR = __CommonTableAttributes._CATEGORY_SYMBOL_COLOR
    __CATEGORY_SYMBOL_BORDER = __CommonTableAttributes._CATEGORY_SYMBOL_BORDER
    __CATEGORY_SYMBOL_FILL_COLOR = __CommonTableAttributes._CATEGORY_SYMBOL_FILL_COLOR

    __CATALOGUE_KEYS = {__CATEGORY_LABEL, __CATEGORY_SYMBOL_SHAPE,
                        __CATEGORY_SYMBOL_COLOR, __CATEGORY_SYMBOL_SIZE,
                        __CATEGORY_SYMBOL_BORDER, __CATEGORY_SYMBOL_FILL_COLOR}

    __OBJECTIVES_KEY = __CommonTableAttributes._OBJECTIVES_KEY
    __OBJECTIVE_TYPE_KEY = __CommonTableAttributes._TYPE_KEY
    __OBJECTIVE_TYPES = __CommonTableAttributes._OBJECTIVE_TYPES
    __OBJECTIVE_EXPRESSION_KEY = __CommonTableAttributes._EXPRESSION_KEY
    __OBJECTIVE_FORMAT_KEY = __CommonTableAttributes._FORMAT_KEY
    __OBJECTIVE_DESCRIPTION_KEY = __CommonTableAttributes._DESCRIPTION_KEY
    __MANDATORY_OBJECTIVE_KEYS = (__OBJECTIVE_TYPE_KEY, __OBJECTIVE_EXPRESSION_KEY)
    __ALL_OBJECTIVE_KEYS = (*__MANDATORY_OBJECTIVE_KEYS, __OBJECTIVE_FORMAT_KEY, __OBJECTIVE_DESCRIPTION_KEY)

    __CONSTRAINTS_KEY = __CommonTableAttributes._CONSTRAINTS_KEY
    __CONSTRAINT_TYPE_KEY = __CommonTableAttributes._TYPE_KEY
    __CONSTRAINT_TYPES = __CommonTableAttributes._CONSTRAINT_TYPES
    __CONSTRAINT_TOLERANCE_KEY = __CommonTableAttributes._TOLERANCE_KEY
    __CONSTRAINT_LIMIT_KEY = __CommonTableAttributes._LIMIT_KEY
    __CONSTRAINT_EXPRESSION_KEY = __CommonTableAttributes._EXPRESSION_KEY
    __CONSTRAINT_FORMAT_KEY = __CommonTableAttributes._FORMAT_KEY
    __CONSTRAINT_DESCRIPTION_KEY = __CommonTableAttributes._DESCRIPTION_KEY
    __MANDATORY_CONSTRAINT_KEYS = (__CONSTRAINT_TYPE_KEY, __CONSTRAINT_TOLERANCE_KEY, __CONSTRAINT_LIMIT_KEY, __CONSTRAINT_EXPRESSION_KEY)
    __ALL_CONSTRAINT_KEYS = (*__MANDATORY_CONSTRAINT_KEYS, __CONSTRAINT_FORMAT_KEY, __CONSTRAINT_DESCRIPTION_KEY)

    __EXPRESSIONS_KEY = "expressions"
    __EXPRESSION_EXPRESSION_KEY = __CommonTableAttributes._EXPRESSION_KEY
    __EXPRESSION_FORMAT_KEY = __CommonTableAttributes._FORMAT_KEY
    __EXPRESSION_DESCRIPTION_KEY = __CommonTableAttributes._DESCRIPTION_KEY

    def __init__(self, table_name, encoded_column_names, rows, optional_properties=None,
                 objectives=None, constraints=None, expressions=None):
        self.table_name = table_name
        self.encoded_column_names = encoded_column_names
        self.rows = rows
        self.optional_properties = optional_properties
        self.objectives = objectives
        self.constraints = constraints
        self.expressions = expressions
        self.__symbol_converter = _SymbolConverter()

    def check(self):
        self.__check_table_name()
        self._check_duplicated_columns(self.encoded_column_names)
        for name in self.encoded_column_names:
            self.__check_column_name(name)
        variable_names = self.__check_duplicated_variable_names()
        self._check_rows_length(self.encoded_column_names, self.rows)
        self.__check_column_values()
        if self.optional_properties is not None:
            self.__parse_extra_properties(variable_names)
        if self.objectives is not None:
            self.__check_objectives()
        if self.constraints is not None:
            self.__check_constraints()
        if self.expressions is not None:
            self.__check_expressions()

    def __check_table_name(self):
        _arg_parse.ensure_correct_args(("table_name", "string", self.table_name), )
        if len(self.table_name.strip()) == 0:
            raise ValueError("'table_name' can't be empty")

    def __check_column_name(self, column_name):
        if column_name in {self.__ID_COLUMN_NAME, self.__MARKED_COLUMN_NAME, self.__VIRTUAL_COLUMN_NAME}:
            return
        for prefix in (self.__CATALOGUE_COLUMN_PREFIX, self.__INPUT_COLUMN_PREFIX, self.__OUTPUT_COLUMN_PREFIX):
            prefix_length = len(prefix)
            if column_name[:prefix_length] == prefix and len(column_name[prefix_length:].strip()) > 0:
                return
        raise ValueError("invalid column name '%s'" % (column_name,))

    def __check_duplicated_variable_names(self):
        variable_names = set()
        for name in self.encoded_column_names:
            for prefix in (self.__CATALOGUE_COLUMN_PREFIX, self.__INPUT_COLUMN_PREFIX, self.__OUTPUT_COLUMN_PREFIX):
                if name.startswith(prefix):
                    var_name = name[len(prefix):]
                    if var_name in variable_names:
                        raise ValueError("duplicate variable name '%s'" % (var_name,))
                    else:
                        variable_names.add(var_name)
        return variable_names

    def __check_column_values(self):
        checks = [[lambda name: name == self.__ID_COLUMN_NAME, lambda value: isinstance(value, int) and not isinstance(value, bool), lambda value: value >= 0],
                  [lambda name: name == self.__MARKED_COLUMN_NAME, lambda value: isinstance(value, bool), None],
                  [lambda name: name == self.__VIRTUAL_COLUMN_NAME, lambda value: isinstance(value, bool), None],
                  [lambda name: name[:len(self.__CATALOGUE_COLUMN_PREFIX)] == self.__CATALOGUE_COLUMN_PREFIX, lambda value: value is None or isinstance(value, str), None],
                  [lambda name: name[:len(self.__INPUT_COLUMN_PREFIX)] == self.__INPUT_COLUMN_PREFIX, lambda value: isinstance(value, _numbers.Number) and not isinstance(value, bool), None],
                  [lambda name: name[:len(self.__OUTPUT_COLUMN_PREFIX)] == self.__OUTPUT_COLUMN_PREFIX, lambda value: isinstance(value, _numbers.Number) and not isinstance(value, bool), None]]

        for index, column_name in enumerate(self.encoded_column_names):
            for check in checks:
                name_predicate = check[0]
                if name_predicate(column_name):
                    type_predicate = check[1]
                    self.__ensure_valid_columns_types(index, type_predicate)
                    value_predicate = check[2]
                    if value_predicate:
                        self.__ensure_valid_columns_values(index, value_predicate)

    def __ensure_valid_columns_types(self, column_index, type_predicate):
        column = [row[column_index] for row in self.rows]
        for row_index, value in enumerate(column):
            if not type_predicate(value):
                column_name = self.encoded_column_names[column_index]
                raise TypeError("Invalid type for value '%s' in column '%s' at row %d" % (value, column_name, row_index + 1))

    def __ensure_valid_columns_values(self, column_index, value_predicate):
        column = [row[column_index] for row in self.rows]
        for row_index, value in enumerate(column):
            if not value_predicate(value):
                column_name = self.encoded_column_names[column_index]
                raise ValueError("Invalid value '%s' for '%s' at row %d" % (value, column_name, row_index + 1))

    def __parse_extra_properties(self, variable_names):
        if not isinstance(self.optional_properties, dict):
            raise TypeError("This method requires a dictionary with properties as third parameter")

        for target_var, property_dict in self.optional_properties.items():
            if not isinstance(target_var, str):
                raise TypeError("Invalid type for value '%s'" % (target_var,))

            if target_var not in variable_names:
                raise ValueError("'%s' is not a valid variable or catalogue" % (target_var,))

            if not isinstance(property_dict, dict):
                raise TypeError("Invalid properties definition for '%s'" % (target_var,))

            encoded_catalogue = self.__CATALOGUE_COLUMN_PREFIX + target_var
            if encoded_catalogue not in self.encoded_column_names:
                self.__check_variables_options(property_dict.items(), target_var)
            else:
                self.__check_catalogues_options(target_var, property_dict)
        self.__parse_optional_dictionary()

    def __check_variables_options(self, properties, target_var):
        for property_name, property_value in properties:
            if not isinstance(property_name, str):
                raise TypeError("'%s' is not a valid property" % (property_name,))
            if property_name not in self.__ALL_PARAMETER_KEYS:
                raise ValueError("'%s' is not a valid property" % (property_name,))
            input_properties = (self.__TYPE_KEY, self.__DEFAULT_VALUE_KEY, self.__BOUNDS_KEY, self.__BASE_KEY)
            if property_name in input_properties and not self.__is_input_var(target_var):
                raise ValueError("Invalid property '%s' for variable '%s'" % (property_name, target_var))
            self.__check_property_values(property_name, property_value)

    def __check_property_values(self, name, value):
        error_message = "Invalid value '%s' for property '%s'" % (value, name)

        if name in {self.__FORMAT_KEY, self.__DESCRIPTION_KEY, self.__TYPE_KEY} \
                and not isinstance(value, str):
            raise TypeError(error_message)

        if name == self.__TYPE_KEY and value not in self.__VALID_TYPES:
            raise ValueError(error_message)

        if name == self.__DEFAULT_VALUE_KEY and not self.__is_valid_number(value):
            raise TypeError(error_message)

        if name == self.__BOUNDS_KEY:
            self.__check_bounds(value)

        if name == self.__BASE_KEY:
            if not isinstance(value, int):
                raise TypeError(error_message)
            if value < 0:
                raise ValueError(error_message)

    def __check_bounds(self, value):
        try:
            bounds = tuple(value)
        except:
            raise TypeError("Invalid bounds '%s'" % (value,))
        if len(bounds) != 2:
            raise ValueError("Invalid length for bounds '%s'" % (value,))
        if not (self.__is_valid_number(bounds[0]) and self.__is_valid_number(bounds[1])):
            raise TypeError("Invalid bounds '%s'" % (value,))

    def __is_valid_number(self, value):
        return isinstance(value, _numbers.Number)

    def __check_catalogues_options(self, target_var, property_dict):
        catalogue_properties_check = {
            self.__CATEGORY_LABEL: self.__check_string,
            self.__CATEGORY_SYMBOL_SHAPE: self.__check_string,
            self.__CATEGORY_SYMBOL_SIZE: self.__check_non_negative_number,
            self.__CATEGORY_SYMBOL_BORDER: self.__check_non_negative_number,
            self.__CATEGORY_SYMBOL_COLOR: self.__check_color,
            self.__CATEGORY_SYMBOL_FILL_COLOR: self.__check_color
        }

        for category, category_properties in property_dict.items():
            if not isinstance(category, str):
                raise TypeError("Invalid value '%s' for a category" % (category,))
            for property_name, property_value in category_properties.items():
                if not isinstance(property_name, str):
                    raise TypeError("'%s' is not a valid  category property" % (property_name,))
                if property_name not in self.__CATALOGUE_KEYS:
                    raise ValueError("'%s' is not a category of '%s'" % (property_name, target_var))
                catalogue_properties_check[property_name](property_name, property_value)

    def __check_string(self, property_name, property_value):
        if not (property_value is None or isinstance(property_value, str)):
            raise TypeError("'%s' is not a valid %s" % (property_value, property_name))

    def __check_non_negative_number(self, property_name, property_value):
        self.__check_number(property_name, property_value)
        if property_value is not None and property_value < 0:
            raise ValueError("'%s' is not a valid %s" % (property_value, property_name))

    def __check_number(self, property_name, property_value):
        if not (property_value is None or self.__is_valid_number(property_value)):
            raise TypeError("'%s' is not a valid %s" % (property_value, property_name))

    def __check_color(self, property_name, property_value):
        if property_value is None:
            return
        if not self.__is_valid_color_type(property_value):
            raise TypeError("'%s' is not a valid %s (must be a string or a tuple)" % (property_value, property_name))
        if not self.__is_valid_color_value(property_value):
            raise ValueError("'%s' is not a valid %s" % (property_value, property_name))

    def __is_valid_color_type(self, value):
        return isinstance(value, str) or self.__is_tuple_like(value)

    def __is_tuple_like(self, value):
        try:
            tuple(value)
            return True
        except:
            return False

    def __is_valid_color_value(self, value):
        if isinstance(value, str):
            return _re.match(r"#[\da-fA-F]{3,4}", value)
        else:
            n = len(value)
            return (n == 3 or n == 4) and all([self.__is_valid_number(i) for i in value])

    def __is_input_var(self, target_var):
        return self.__INPUT_COLUMN_PREFIX + target_var in self.encoded_column_names

    def __parse_optional_dictionary(self):
        if self.optional_properties is not None:
            for variable_dict in self.optional_properties.values():
                if self.__BOUNDS_KEY in variable_dict.keys():
                    try:
                        variable_dict[self.__BOUNDS_KEY] = tuple(variable_dict[self.__BOUNDS_KEY])
                    except:
                        raise ValueError("Invalid bounds definition '%s'" % (variable_dict[self.__BOUNDS_KEY],))

    def __check_objectives(self):
        if not isinstance(self.objectives, dict):
            raise TypeError("Invalid objectives format")
        for obj_name, obj_dict in self.objectives.items():
            if not isinstance(obj_name, str):
                raise TypeError("Invalid type for objective name")
            if not isinstance(obj_dict, dict):
                raise TypeError("Invalid format for objective '%s' properties" % (obj_name,))
            self.__parse_objective_properties(obj_dict)

    def __parse_objective_properties(self, obj_dict):
        missing_obj_properties = [prop for prop in self.__MANDATORY_OBJECTIVE_KEYS if prop not in obj_dict]
        if missing_obj_properties:
            raise RuntimeError("Missing objective properties: '%s'" % ("', '".join(missing_obj_properties),))
        for property_name, property_value in obj_dict.items():
            if property_name not in self.__ALL_OBJECTIVE_KEYS:
                raise ValueError("'%s' is not a valid objective property" % (property_name,))
            if (property_name == self.__OBJECTIVE_TYPE_KEY
                    and property_value not in self.__OBJECTIVE_TYPES or
                    not isinstance(property_value, str)):
                raise ValueError("Invalid value '%s' for objective property '%s'" % (property_value, property_name))

    def __check_constraints(self):
        if not isinstance(self.constraints, dict):
            raise TypeError("Invalid constraints format")
        for constr_name, constr_dict in self.constraints.items():
            if not isinstance(constr_name, str):
                raise TypeError("Invalid type for constraint name")
            if not isinstance(constr_dict, dict):
                raise TypeError("Invalid format for constraint '%s' properties" % (constr_name,))
            self.__parse_constraints_properties(constr_dict)

    def __parse_constraints_properties(self, constr_dict):
        missing_constr_properties = [prop for prop in self.__MANDATORY_CONSTRAINT_KEYS if prop not in constr_dict]
        if missing_constr_properties:
            raise RuntimeError("Missing constraint properties: '%s'" % ("', '".join(missing_constr_properties),))
        string_properties = (self.__CONSTRAINT_EXPRESSION_KEY, self.__CONSTRAINT_FORMAT_KEY, self.__CONSTRAINT_DESCRIPTION_KEY)
        for property_name, property_value in constr_dict.items():
            if property_name not in self.__ALL_CONSTRAINT_KEYS:
                raise ValueError("'%s' is not a valid constraint property" % (property_name,))
            if property_name == self.__CONSTRAINT_TYPE_KEY and property_value not in self.__CONSTRAINT_TYPES or \
                    property_name == self.__CONSTRAINT_TOLERANCE_KEY and not self.__is_valid_number(property_value) or \
                    property_name == self.__CONSTRAINT_LIMIT_KEY and not self.__is_valid_number(property_value) or \
                    property_name in string_properties and not isinstance(property_value, str):
                raise ValueError("Invalid value '%s' for constraint property '%s'" % (property_value, property_name))

    def __check_expressions(self):
        if not isinstance(self.expressions, dict):
            raise TypeError("Invalid expressions format")
        for expr_name, expr_dict in self.expressions.items():
            if not isinstance(expr_name, str):
                raise TypeError("Invalid type for expression name")
            if not isinstance(expr_dict, dict):
                raise TypeError("Invalid format for expression '%s' properties" % (expr_name,))
            self.__parse_expression_properties(expr_dict)

    def __parse_expression_properties(self, expr_dict):
        if self.__EXPRESSION_EXPRESSION_KEY not in expr_dict:
            raise RuntimeError("Missing expression property: '%s'" % (self.__EXPRESSION_EXPRESSION_KEY,))
        for property_name, property_value in expr_dict.items():
            if property_name not in (self.__EXPRESSION_EXPRESSION_KEY, self.__EXPRESSION_FORMAT_KEY, self.__EXPRESSION_DESCRIPTION_KEY):
                raise ValueError("'%s' is not a valid expression property" % (property_name,))
            if not isinstance(property_value, str):
                raise ValueError("Invalid value '%s' for expression property '%s'" % (property_value, property_name))

    def build(self):
        spec = {self.__INPUTS_KEY: {},
                self.__OUTPUTS_KEY: {},
                self.__CATEGORIES_KEY: {}}
        for index, name in enumerate(self.encoded_column_names):
            variable_added = self.__add_fixed_field_to_spec(spec, index, name) \
                             or self.__add_variable_to_spec(spec, index, name) \
                             or self.__add_category_to_spec(spec, index, name)
            if not variable_added:
                raise RuntimeError("unexpected row name")
        if self.optional_properties:
            self.__add_optional_properties_to_spec(spec)
        if self.objectives:
            spec[self.__OBJECTIVES_KEY] = self.objectives
        if self.constraints:
            spec[self.__CONSTRAINTS_KEY] = self.constraints
        if self.expressions:
            spec[self.__EXPRESSIONS_KEY] = self.expressions
        return _db.create_table(self.table_name, spec)

    def __add_fixed_field_to_spec(self, spec, index, name):
        """Return whether more processing is necessary for the column."""
        if name == self.__ID_COLUMN_NAME:
            spec[self.__ID_KEY] = self.__get_column(index)
            return True

        if name == self.__MARKED_COLUMN_NAME:
            spec[self.__MARKED_KEY] = self.__get_column(index)
            return True

        if name == self.__VIRTUAL_COLUMN_NAME:
            spec[self.__VIRTUAL_KEY] = self.__get_column(index)
            return True

        return False

    def __add_variable_to_spec(self, spec, index, name):
        input_name = self.__get_column_name(name, self.__INPUT_COLUMN_PREFIX)
        if input_name:
            input = {self.__DATA_KEY: self.__get_column(index)}
            spec[self.__INPUTS_KEY][input_name] = input
            return True

        output_name = self.__get_column_name(name, self.__OUTPUT_COLUMN_PREFIX)
        if output_name:
            output = {self.__DATA_KEY: self.__get_column(index)}
            spec[self.__OUTPUTS_KEY][output_name] = output
            return True

        return False

    def __add_category_to_spec(self, spec, index, name):
        catalogue_name = self.__get_column_name(name, self.__CATALOGUE_COLUMN_PREFIX)
        if catalogue_name:
            catalogue = {}
            names = self.__get_column(index)
            catalogue[self.__CATEGORY_NAMES_KEY] = names
            every_category_set = set([x for x in names if x is not None])
            if self.optional_properties and catalogue_name in self.optional_properties:
                every_category_set.update(self.optional_properties[catalogue_name].keys())
                categories = self.__get_categories_for_catalogue(catalogue_name)
                catalogue[self.__CATEGORY_LABELS_KEY] = self.__build_labels(self.optional_properties[catalogue_name], categories)
                catalogue[self.__CATEGORY_SYMBOLS_KEY] = self.__build_symbol_strings(self.optional_properties[catalogue_name], categories)
            else:
                catalogue[self.__CATEGORY_LABELS_KEY] = {}
                catalogue[self.__CATEGORY_SYMBOLS_KEY] = {}
            catalogue[self.__EVERY_CATEGORY_KEY] = tuple(every_category_set)
            spec[self.__CATEGORIES_KEY][catalogue_name] = catalogue
            return True
        return False

    def __get_categories_for_catalogue(self, catalogue_name):
        return set(self.optional_properties[catalogue_name].keys())

    def __build_labels(self, catalogue_properties, categories):
        results = {}
        for category in categories:
            label = catalogue_properties.get(category, {}).get(self.__CATEGORY_LABEL, None)
            if label:
                results[category] = label
        return results

    def __build_symbol_strings(self, catalogue_properties, categories):
        results = {}
        for category in categories:
            category_properties = catalogue_properties.get(category, {}).copy()
            if self.__CATEGORY_LABEL in category_properties:
                del (category_properties[self.__CATEGORY_LABEL])
            if len(category_properties) > 0:
                results[category] = self.__symbol_converter.dict_to_string(category_properties)
        return results

    def __add_optional_properties_to_spec(self, spec):
        inputs = spec[self.__INPUTS_KEY]
        outputs = spec[self.__OUTPUTS_KEY]
        for variable_name, property_dict in self.optional_properties.items():
            if (self.__CATALOGUE_COLUMN_PREFIX + variable_name) not in self.encoded_column_names:
                if variable_name in inputs.keys():
                    self.__add_property_to_spec_dict(inputs[variable_name], property_dict)
                elif variable_name in outputs.keys():
                    self.__add_property_to_spec_dict(outputs[variable_name], property_dict)
                else:
                    raise ValueError("'%s' is not an input variable or an output variable" % (variable_name,))

    def __add_property_to_spec_dict(self, variable, property_dict):
        for property_name, property_value in property_dict.items():
            variable[property_name] = property_value

    def __get_column(self, index):
        return tuple([i[index] for i in self.rows])

    def __get_column_name(self, name, prefix):
        prefix_length = len(prefix)
        if name[:prefix_length] == prefix:
            return name[prefix_length:].strip()
