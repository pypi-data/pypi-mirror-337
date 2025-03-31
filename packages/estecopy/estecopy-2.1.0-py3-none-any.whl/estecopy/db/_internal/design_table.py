import copy as _copy
from estecopy._internal import _db
from estecopy._utils import arg_parse as _arg_parse
from estecopy.db._internal import attributes as _attributes
from estecopy.db._internal.design_table_encoder import _DesignTableEncoder
from estecopy.db._internal.encoded_header_table_builder import _EncodedHeaderTableBuilder
from estecopy.db._internal.progress_loader import _ProgressLoader
from estecopy.db._internal.symbol_converter import _SymbolConverter


class DesignTable:
    """This class represents a table loaded to pyCONSOLE from the Design Space.

To load a table use the method db.get_table(tableName).
"""

    __METADATA_KEY = _attributes.METADATA_KEY
    __CATEGORIES_KEY = _attributes.CATEGORIES_KEY
    __COLUMN_NAMES_KEY = _attributes.COLUMN_NAMES_KEY
    __MARKED_KEY = _attributes.MARKED_KEY
    __LINKED_SESSION_TABLE_NAME_KEY = _attributes.LINKED_SESSION_TABLE_NAME_KEY

    __NAME_KEY = _attributes.NAME_KEY
    __ROWS_KEY = _attributes.ROWS_KEY
    __ID_KEY = _attributes.ID_KEY
    __RID_KEY = _attributes.RID_KEY
    __IDS_KEY = _attributes.IDS_KEY
    __VIRTUAL_KEY = _attributes.VIRTUAL_KEY

    __CommonTableAttributes = _attributes._CommonTableAttributes

    __GOALS_KEY = "goals"
    __INPUTS_KEY = "input_variables"
    __INPUT_LOWER_BOUND_KEY = "lower_bound"
    __INPUT_UPPER_BOUND_KEY = "upper_bound"
    __OUTPUTS_KEY = "output_variables"
    __EXPRESSIONS_KEY = "trans_variables"
    __CONSTRAINTS_KEY = __CommonTableAttributes._CONSTRAINTS_KEY
    __OBJECTIVES_KEY = __CommonTableAttributes._OBJECTIVES_KEY
    __ALL_VARIABLES_TYPES_KEYS = (__INPUTS_KEY, __OUTPUTS_KEY, __EXPRESSIONS_KEY, __CONSTRAINTS_KEY, __OBJECTIVES_KEY)
    __USER_TYPE_FOR_VARIABLE_TYPE_KEY = {__INPUTS_KEY: "input",
                                         __OUTPUTS_KEY: "output",
                                         __EXPRESSIONS_KEY: "expression",
                                         __CONSTRAINTS_KEY: "constraint",
                                         __OBJECTIVES_KEY: "objective"}

    __IS_VECTOR_COMPONENT_PROPERTY_KEY = "is_vector_component"
    __VECTOR_ID_PROPERTY_KEY = "vector_id"
    __STEP_KEY = "step"
    __INPUT_TYPES = ("variable", "constant", "expression")
    __DEFAULT_VALUE_KEY = __CommonTableAttributes._DEFAULT_VALUE_KEY
    __INPUT_TYPE_KEY = __CommonTableAttributes._TYPE_KEY
    __TOLERANCE_KEY = __CommonTableAttributes._TOLERANCE_KEY
    __EXPRESSION_KEY = __CommonTableAttributes._EXPRESSION_KEY
    __LIMIT_KEY = __CommonTableAttributes._LIMIT_KEY
    __CONSTRAINT_TYPE_KEY = __CommonTableAttributes._TYPE_KEY
    __CONSTRAINT_TYPES = __CommonTableAttributes._CONSTRAINT_TYPES
    __OBJECTIVE_TYPE_KEY = __CommonTableAttributes._TYPE_KEY
    __OBJECTIVE_TYPES = __CommonTableAttributes._OBJECTIVE_TYPES
    __FORMAT_KEY = __CommonTableAttributes._FORMAT_KEY
    __DESCRIPTION_KEY = __CommonTableAttributes._DESCRIPTION_KEY
    __BASE_KEY = __CommonTableAttributes._BASE_KEY

    __CATALOGUES_KEY = "catalogues"
    __CATALOGUE_NAME = "name"
    __EMPTY_CATEGORY_FLAG = -1
    __CATEGORY_NAME_KEY = "name"
    __CATEGORY_TITLE_KEY = "title"
    __CATEGORY_SYMBOL_KEY = "symbol"
    __CATEGORY_LABEL = __CommonTableAttributes._CATEGORY_LABEL
    __CATEGORY_SYMBOL_SHAPE = __CommonTableAttributes._CATEGORY_SYMBOL_SHAPE
    __CATEGORY_SYMBOL_SIZE = __CommonTableAttributes._CATEGORY_SYMBOL_SIZE
    __CATEGORY_SYMBOL_COLOR = __CommonTableAttributes._CATEGORY_SYMBOL_COLOR
    __CATEGORY_SYMBOL_BORDER = __CommonTableAttributes._CATEGORY_SYMBOL_BORDER
    __CATEGORY_SYMBOL_FILL_COLOR = __CommonTableAttributes._CATEGORY_SYMBOL_FILL_COLOR
    __CATEGORY_PROPERTIES_KEYS = {__CATEGORY_LABEL, __CATEGORY_SYMBOL_SHAPE, __CATEGORY_SYMBOL_SIZE,
                                  __CATEGORY_SYMBOL_COLOR, __CATEGORY_SYMBOL_BORDER, __CATEGORY_SYMBOL_FILL_COLOR}

    __TYPE_USER_PROPERTY = "type"
    __CATALOGUE_NAMES_USER_PROPERTY = "names"
    __CATALOGUE_LABELS_USER_PROPERTY = "labels"
    __CATALOGUE_TITLES_USER_PROPERTY = "titles"
    __CATALOGUE_SYMBOLS_USER_PROPERTY = "symbols"
    __BOUNDS_USER_PROPERTY = "bounds"
    __VECTOR_INDEX_USER_PROPERTY = "vector_index"
    __DEFAULT_VALUE_USER_PROPERTY = "default_value"
    __INPUT_TYPE_USER_PROPERTY = "input_type"
    __EXPRESSION_USER_PROPERTY = "expression"
    __LIMIT_USER_PROPERTY = "limit"
    __TOLERANCE_USER_PROPERTY = "tolerance"
    __OBJECTIVE_TYPE_USER_PROPERTY = "objective_type"
    __CONSTRAINT_TYPE_USER_PROPERTY = "constraint_type"
    __FORMAT_USER_PROPERTY = "format"
    __DESCRIPTION_USER_PROPERTY = "description"
    __BASE_USER_PROPERTY = "base"
    __STEP_USER_PROPERTY = "step"

    __PLAIN_TABLE_ID_INDEX = 0
    __PLAIN_TABLE_MARKED_INDEX = 1
    __PLAIN_TABLE_VIRTUAL_INDEX = 2
    __PLAIN_TABLE_FIRST_CATEGORY_INDEX = 3

    def __init__(self, name, show_progress=True, show_robust_ids=False, preload_linked_table=True, clone=None):
        self.__name = name
        self.__show_progress = show_progress
        self.__show_robust_ids = show_robust_ids
        self.__linked_table = None
        self.__load_table(name, preload_linked_table, clone)
        self.__symbol_converter = _SymbolConverter()

    def __dir__(self):
        return [i for i in DesignTable.__dict__.keys() if not i.startswith("_DesignTable__")]

    def __delitem__(self, key):
        if self.__is_robust() or self.__has_extra_ids():
            raise NotImplementedError("Changing robust tables or their linked tables is not supported")
        else:
            self.__update_id_cache(key)
            del self.__raw_data[self.__ROWS_KEY][key]

    def __update_id_cache(self, key):
        if isinstance(key, slice):
            rows_slice = self.__raw_data[self.__ROWS_KEY][key]
            for element in rows_slice:
                self.__id_cache.remove(element[1][self.__ID_KEY])
        else:
            self.__id_cache.remove(self.__raw_data[self.__ROWS_KEY][key][1][self.__ID_KEY])

    def __getitem__(self, item):
        if _arg_parse.is_string(item):
            return self.__get_catalogue_data(item)
        elif isinstance(item, tuple):
            return self.__handle_tuple_index(item)
        else:
            return self.get_rows()[1:][item]

    def __get_catalogue_data(self, catalogue_name):
        if catalogue_name not in self.get_catalogues():
            raise KeyError(f"{catalogue_name}")
        catalogue_data = self.get_catalogue_property(catalogue_name, self.__CATALOGUE_SYMBOLS_USER_PROPERTY)
        labels = self.get_catalogue_property(catalogue_name, self.__CATALOGUE_LABELS_USER_PROPERTY)
        for k, v in catalogue_data.items():
            v[self.__CATEGORY_LABEL] = labels[k]
        return catalogue_data

    def __handle_tuple_index(self, item):
        if len(item) == 0:
            raise IndexError("No index provided")
        elif _arg_parse.is_string(item[0]):
            return self.__handle_catalogue_tuple(item)
        else:
            return self.__handle_indices_tuple(item)

    def __handle_catalogue_tuple(self, item):
        data = self.__get_catalogue_data(item[0])
        for key in item[1:]:
            data = data[key]
        return data

    def __handle_indices_tuple(self, item):
        if len(item) != 2:
            raise IndexError(f"Too many indices: 2 expected, {len(item)} provided")
        row_index, column_index = item
        current_rows = self.get_rows()[1:][row_index]
        if isinstance(row_index, slice):
            return tuple(row[column_index] for row in current_rows)
        else:
            return current_rows[column_index]

    def __setitem__(self, key, value):
        if self.__is_robust() or self.__has_extra_ids():
            raise NotImplementedError("Changing robust tables or their linked tables is not supported")
        elif isinstance(key, tuple):
            self.__handle_tuple_setitem(key, value)
        elif value is None:
            self.__delitem__(key)
        else:
            self.__set_row(key, value)

    def __handle_tuple_setitem(self, key, value):
        if len(key) == 0:
            raise IndexError("No index provided")
        elif _arg_parse.is_string(key[0]):
            self.__handle_category_setitem(key, value)
        else:
            self.__set_cell(key, value)

    def __handle_category_setitem(self, key, new_properties):
        if len(key) == 2:
            self.__set_category_properties(key[0], key[1], new_properties)
        elif len(key) == 3:
            self.__set_category_properties(key[0], key[1], {key[2]: new_properties})
        else:
            raise IndexError(f"Too many indices: expected at most 3, but {len(key)} provided")

    def __set_category_properties(self, catalogue_name, category_name, new_properties):
        self.__check_category_name(category_name)
        catalogue_data = self.__get_catalogue_data(catalogue_name)
        category_properties = catalogue_data.get(category_name, {self.__CATEGORY_LABEL: ''})
        self.__update_valid_category_properties(category_properties, new_properties)
        if category_name not in catalogue_data:
            self.__set_new_category_properties(catalogue_name, category_name, category_properties)
        else:
            self.__update_existing_category_properties(catalogue_name, category_name, category_properties)

    def __update_valid_category_properties(self, category_properties, new_properties):
        if not isinstance(new_properties, dict):
            raise TypeError("Invalid type for category properties")
        for property in new_properties:
            if property not in self.__CATEGORY_PROPERTIES_KEYS:
                raise KeyError(f"{property}")
            category_properties[property] = new_properties[property]

    def __set_new_category_properties(self, catalogue_name, category_name, new_category_properties):
        catalogues = list(self.__get_catalogues())
        catalogue_index = self.__get_catalogue_names().index(catalogue_name)
        raw_category_data = {self.__CATEGORY_LABEL: '', self.__CATEGORY_NAME_KEY: category_name,
                             self.__CATEGORY_SYMBOL_KEY: self.__symbol_converter.dict_to_string({}), self.__CATEGORY_TITLE_KEY: category_name}
        categories_of_catalogue = list(catalogues[catalogue_index][self.__CATEGORIES_KEY])
        categories_of_catalogue.append(self.__update_category_data(raw_category_data, new_category_properties))
        self.__update_raw_category_data(catalogue_index, catalogues, categories_of_catalogue)

    def __update_existing_category_properties(self, catalogue_name, category_name, new_category_properties):
        catalogues = list(self.__get_catalogues())
        catalogue_index, category_index, raw_category_data = self.__extract_relevant_category(catalogue_name, category_name, catalogues)
        categories_of_catalogue = list(catalogues[catalogue_index][self.__CATEGORIES_KEY])
        categories_of_catalogue[category_index] = self.__update_category_data(raw_category_data, new_category_properties)
        self.__update_raw_category_data(catalogue_index, catalogues, categories_of_catalogue)

    def __update_raw_category_data(self, catalogue_index, catalogues, categories_of_catalogue):
        catalogues[catalogue_index][self.__CATEGORIES_KEY] = tuple(categories_of_catalogue)
        self.__raw_data[self.__CATALOGUES_KEY] = tuple(catalogues)

    def __extract_relevant_category(self, catalogue_name, category_name, catalogues):
        catalogue_index = self.__get_catalogue_names().index(catalogue_name)
        relevant_catalogue = catalogues[catalogue_index]
        category_index = self.__get_category_index(self.__get_catalogue_data(catalogue_name), catalogue_name, category_name)
        raw_category_data = relevant_catalogue[self.__CATEGORIES_KEY][category_index]
        return catalogue_index, category_index, raw_category_data

    def __update_category_data(self, raw_category_data, new_category_properties):
        self.__check_category_label(new_category_properties[self.__CATEGORY_LABEL])
        raw_category_data[self.__CATEGORY_LABEL] = new_category_properties[self.__CATEGORY_LABEL]
        del new_category_properties[self.__CATEGORY_LABEL]
        symbol_as_dict = self.__symbol_converter.string_to_dict(raw_category_data[self.__CATEGORY_SYMBOL_KEY])
        symbol_as_dict.update(new_category_properties)
        raw_category_data[self.__CATEGORY_SYMBOL_KEY] = self.__symbol_converter.dict_to_string(symbol_as_dict)
        return raw_category_data

    def __check_category_label(self, category_label):
        if not _arg_parse.is_string(category_label):
            raise TypeError("Invalid type for category label")

    def __set_cell(self, key, value):
        if len(key) != 2:
            raise IndexError(f"Too many indices: 2 expected, {len(key)} provided")
        header = self.__create_rows_header(self.__show_robust_ids)
        row_index, column_index = key[0], self.__validate_column_index(key[1], len(header))
        first_numeric_index = self.__get_first_numeric_index(header)
        if column_index == self.__PLAIN_TABLE_ID_INDEX:
            self.__set_id(row_index, value)
        elif column_index == self.__PLAIN_TABLE_MARKED_INDEX:
            self.__set_status(row_index, value, "Invalid type for marked status field", self.__MARKED_KEY)
        elif column_index == self.__PLAIN_TABLE_VIRTUAL_INDEX:
            self.__set_status(row_index, value, "Invalid type for virtual status field", self.__VIRTUAL_KEY)
        elif column_index in range(self.__PLAIN_TABLE_FIRST_CATEGORY_INDEX, first_numeric_index):
            self.__set_category(row_index, column_index, header, value)
        else:
            self.__set_numeric_value(row_index, column_index, first_numeric_index, value)

    def __get_first_numeric_index(self, header):
        return len(header) - len(self.get_variables())

    def __validate_column_index(self, column_index, row_length):
        if column_index < -row_length or column_index >= row_length:
            raise IndexError("list index out of range")
        return column_index % row_length

    def __set_id(self, row_index, new_id):
        current_raw_row = self.__raw_data[self.__ROWS_KEY][row_index]
        old_id = current_raw_row[1][self.__ID_KEY]
        self.__check_id_value(old_id, new_id)
        self.__id_cache.remove(old_id)
        self.__id_cache.add(new_id)
        current_raw_row[1][self.__ID_KEY] = new_id

    def __check_id_value(self, old_id, new_id):
        if not isinstance(new_id, int):
            raise TypeError("Invalid type for row id")
        if new_id < 0:
            raise ValueError(f"Invalid value {new_id} for row id")
        if new_id != old_id and new_id in self.__id_cache:
            raise ValueError(f"Table already contains a row with id = {new_id}")

    def __set_status(self, row_index, value, error, key):
        self.__validate_status(value, error)
        current_raw_row = self.__raw_data[self.__ROWS_KEY][row_index]
        current_raw_row[1][key] = value

    def __validate_status(self, value, error):
        if not isinstance(value, bool):
            raise TypeError(error)

    def __set_category(self, row_index, column_index, header, value):
        catalogue_name = header[column_index]
        catalogue_data = self.__get_catalogue_data(catalogue_name)
        raw_rows = self.__raw_data[self.__ROWS_KEY]
        current_raw_row = raw_rows[row_index]
        category_fields = list(current_raw_row[1][self.__CATEGORIES_KEY])
        category_fields[column_index - self.__PLAIN_TABLE_FIRST_CATEGORY_INDEX] = self.__get_category_index(catalogue_data, catalogue_name, value)
        current_raw_row[1][self.__CATEGORIES_KEY] = tuple(category_fields)
        raw_rows[row_index] = (current_raw_row[0], current_raw_row[1])

    def __get_category_index(self, catalogue_data, catalogue_name, value):
        if value is None:
            return self.__EMPTY_CATEGORY_FLAG
        else:
            self.__check_category_name(value)
            self.__check_category_name_in_catalogue(catalogue_data, catalogue_name, value)
            return tuple(catalogue_data).index(value)

    def __check_category_name(self, value):
        if not _arg_parse.is_string(value):
            raise TypeError("Invalid type for category field")
        if " " in value:
            raise ValueError("Category name cannot contain spaces")

    def __check_category_name_in_catalogue(self, catalogue_data, catalogue_name, value):
        if value not in catalogue_data:
            raise ValueError(f"'{value}' is not a category of '{catalogue_name}'")

    def __set_numeric_value(self, row_index, column_index, first_numeric_index, value):
        self.__validate_value(column_index, value)
        raw_rows = self.__raw_data[self.__ROWS_KEY]
        current_raw_row = raw_rows[row_index]
        numeric_fields = list(current_raw_row[0])
        numeric_fields[column_index - first_numeric_index] = float(value)
        raw_rows[row_index] = (tuple(numeric_fields), current_raw_row[1])

    def __validate_value(self, column_index, value):
        if not _arg_parse.is_float_like(value):
            raise TypeError(f"Invalid type for field at index {column_index}")

    def __set_row(self, row_index, new_row):
        header, *rows = self.get_rows()
        old_id = rows[row_index][self.__PLAIN_TABLE_ID_INDEX]
        new_raw_row = self.__get_new_row(header, old_id, new_row)
        self.__raw_data[self.__ROWS_KEY][row_index] = new_raw_row
        self.__id_cache.remove(old_id)
        self.__id_cache.add(new_row[self.__PLAIN_TABLE_ID_INDEX])

    def __get_new_row(self, header, old_id, new_row):
        self.__validate_row_size(new_row, len(header))
        first_numeric_index = self.__get_first_numeric_index(header)
        categories = self.__validate_row(old_id, new_row, header, first_numeric_index)
        new_raw_row = (tuple((float(el) for el in new_row[first_numeric_index:])),
                       {self.__ID_KEY: new_row[self.__PLAIN_TABLE_ID_INDEX], self.__MARKED_KEY: new_row[self.__PLAIN_TABLE_MARKED_INDEX],
                        self.__VIRTUAL_KEY: new_row[self.__PLAIN_TABLE_VIRTUAL_INDEX], self.__CATEGORIES_KEY: categories, self.__IDS_KEY: ()})
        return new_raw_row

    def __validate_row_size(self, new_row, row_len):
        if not _arg_parse.is_collection(new_row):
            raise TypeError("Invalid row type")
        if len(new_row) != row_len:
            raise ValueError("Invalid row size")

    def __validate_row(self, old_id, row, header, first_numeric_index):
        self.__check_id_value(old_id, row[self.__PLAIN_TABLE_ID_INDEX])
        self.__validate_status(row[self.__PLAIN_TABLE_MARKED_INDEX], "Invalid type for marked status field")
        self.__validate_status(row[self.__PLAIN_TABLE_VIRTUAL_INDEX], "Invalid type for virtual status field")
        categories = []
        for i in range(self.__PLAIN_TABLE_FIRST_CATEGORY_INDEX, first_numeric_index):
            catalogue_name = header[i]
            catalogue_data = self.__get_catalogue_data(catalogue_name)
            categories.append(self.__get_category_index(catalogue_data, catalogue_name, row[i]))
        for i in range(first_numeric_index, len(row)):
            self.__validate_value(i, row[i])
        return tuple(categories)

    def __get_metadata_linked_table_name(self):
        return self.__raw_data[self.__METADATA_KEY][self.__LINKED_SESSION_TABLE_NAME_KEY]

    def __is_robust(self):
        return self.__get_metadata_linked_table_name() is not None

    def get_linked_table_name(self):
        """Returns the name of the work or session table that the robust table is linked to.

It will return 'None' for any other type of table."""
        # Use the actual linked table as the single reputable source
        # of information for the name.
        # Relevant for preload_linked_table = False followed by mF tables changes
        if self.__is_robust():
            return self.get_linked_table().get_name()

    def get_linked_table(self):
        """Returns the work or the session table that the robust table is linked to.

The argument show_robust_ids (explained in the context of the
get_table method) is True by default. It means that the designs in the
loaded table are loaded with their RIDs.

It will return 'None' for any other type of table.
"""
        if not self.__linked_table:
            linked_table_name = self.__get_metadata_linked_table_name()
            if linked_table_name:
                self.__linked_table = DesignTable(linked_table_name, self.__show_progress, preload_linked_table=False, show_robust_ids=True)
        return self.__linked_table

    def __load_table(self, name, preload_linked_table, clone):
        if not clone:
            if self.__show_progress:
                loader = _ProgressLoader(name)
                self.__raw_data = loader.load_table()
            else:
                self.__raw_data = _db.get_table_data(name)
            self.__raw_data[self.__ROWS_KEY] = list(self.__raw_data[self.__ROWS_KEY])
            self.__cache_rows_ids()
            if preload_linked_table:
                self.get_linked_table()

    def __cache_rows_ids(self):
        self.__id_cache = set()
        for raw_row in self.__raw_data[self.__ROWS_KEY]:
            self.__id_cache.add(raw_row[1][self.__ID_KEY])

    def get_name(self):
        """Returns table name."""
        return self.__name

    def set_name(self, table_name):
        """Change the name of the table."""
        _arg_parse.ensure_correct_args(("table_name", "string", table_name), )
        if len(table_name.strip()) == 0:
            raise ValueError("'table_name' can't be empty")
        self.__name = table_name
        self.__raw_data[self.__NAME_KEY] = table_name

    def __create_robust_header_row(self):
        header = [self.__RID_KEY, self.__MARKED_KEY, self.__VIRTUAL_KEY]
        header.extend(self.__get_catalogue_names())
        header.extend(self.__raw_data[self.__METADATA_KEY][self.__COLUMN_NAMES_KEY])
        return tuple(header)

    def __create_robust_header_with_ids_row(self):
        header = [self.__RID_KEY, self.__IDS_KEY, self.__MARKED_KEY, self.__VIRTUAL_KEY]
        header.extend(self.__get_catalogue_names())
        header.extend(self.__raw_data[self.__METADATA_KEY][self.__COLUMN_NAMES_KEY])
        return tuple(header)

    def _create_plain_header_row(self):
        header = [self.__ID_KEY, self.__MARKED_KEY, self.__VIRTUAL_KEY]
        header.extend(self.__get_catalogue_names())
        header.extend(self.__raw_data[self.__METADATA_KEY][self.__COLUMN_NAMES_KEY])
        return tuple(header)

    def __create_plain_meta_columns(self, meta):
        return [meta[self.__ID_KEY], meta[self.__MARKED_KEY], meta[self.__VIRTUAL_KEY]]

    def __create_meta_columns_with_ids(self, meta):
        return [meta[self.__ID_KEY], meta[self.__IDS_KEY], meta[self.__MARKED_KEY], meta[self.__VIRTUAL_KEY]]

    def __create_linked_robust_header_row(self):
        header = [self.__ID_KEY, self.__RID_KEY, self.__MARKED_KEY, self.__VIRTUAL_KEY]
        header.extend(self.__get_catalogue_names())
        header.extend(self.__raw_data[self.__METADATA_KEY][self.__COLUMN_NAMES_KEY])
        return tuple(header)

    def __create_linked_robust_meta_columns(self, meta):
        try:
            rid = meta[self.__IDS_KEY][0]
        except KeyError:
            rid = None
        return [meta[self.__ID_KEY], rid, meta[self.__MARKED_KEY], meta[self.__VIRTUAL_KEY]]

    def __index_row(self):
        index = {}
        linked_rows = self.get_linked_table()._get_rows(False)
        assert (linked_rows[0][0] == "id")
        assert (linked_rows[0][1] != "rid")
        for row in linked_rows[1:]:
            index[row[0]] = row
        return index

    def __extract_robust_designs(self, set_header, linked_index, ids):
        subtable = [set_header]
        for id in ids:
            try:
                subtable.append(linked_index[id])
            except KeyError:
                subtable.append(None)
        return tuple(subtable)

    def __extract_row(self, raw_row, row_reader):
        meta = raw_row[1]
        row_metadata = row_reader(meta)
        categories = self.__decode_categories(meta[self.__CATEGORIES_KEY])
        return tuple(row_metadata + categories + list(raw_row[0]))

    def get_robust_rows(self):
        """Returns table as a sequence of nominal design rows, each followed by its robust samples.

The first row contains column names.

All other rows are pairs of nominal designs and the associated robust samples subtables.

The subtables are analogous to those returned by the get_rows method.
"""
        if not self.__is_robust():
            raise RuntimeError("this method cannot be invoked on non-robust tables")
        else:
            linked_index = self.__index_row()
            set_linked_header = self.get_linked_table()._create_plain_header_row()
            new_rows = [self.__create_robust_header_row()]
            for raw_row in self.__raw_data[self.__ROWS_KEY]:
                header_row = self.__extract_row(raw_row, self.__create_plain_meta_columns)
                ids_tuple = raw_row[1][self.__IDS_KEY]
                sub_table = self.__extract_robust_designs(set_linked_header, linked_index, ids_tuple)
                new_rows.append((header_row, sub_table))
            return tuple(new_rows)

    def __has_extra_ids(self):
        try:
            return len(self.__raw_data[self.__ROWS_KEY][0][1][self.__IDS_KEY]) > 0
        except (IndexError, TypeError):
            return False

    def __create_rows_header(self, show_robust_ids):
        if self.__is_robust():
            if show_robust_ids:
                return self.__create_robust_header_with_ids_row()
            else:
                return self.__create_robust_header_row()
        else:
            if show_robust_ids and self.__has_extra_ids():
                return self.__create_linked_robust_header_row()
            else:
                return self._create_plain_header_row()

    def __create_row_reader(self, show_robust_ids):
        if self.__is_robust():
            if show_robust_ids:
                return self.__create_meta_columns_with_ids
            else:
                return self.__create_plain_meta_columns
        else:
            if show_robust_ids and self.__has_extra_ids():
                return self.__create_linked_robust_meta_columns
            else:
                return self.__create_plain_meta_columns

    def _get_rows(self, show_robust_ids):
        row_reader = self.__create_row_reader(show_robust_ids)
        data = []
        for raw_row in self.__raw_data[self.__ROWS_KEY]:
            data.append(self.__extract_row(raw_row, row_reader))
        data.insert(0, self.__create_rows_header(show_robust_ids))
        return tuple(data)

    def __get_catalogues(self):
        return self.__raw_data[self.__METADATA_KEY][self.__CATALOGUES_KEY]

    def get_rows(self):
        """Returns table as a sequence of rows.

The first row contains column names.

All other rows are designs.

Design ID, RID/robust samples (optionally, if the table was created with
show_robust_ids) whether a design is marked or not and whether a design is
virtual or real are indicated in columns "id", "rid"/"ids", "marked"
and "virtual" respectively.
"""
        return self._get_rows(self.__show_robust_ids)

    def __get_catalogue_names(self):
        return [i[self.__NAME_KEY] for i in self.__get_catalogues()]

    def __decode_categories(self, categories):
        raw_catalogues = self.__get_catalogues()
        names = []
        for catalogue_index, category_index in enumerate(categories):
            if category_index != self.__EMPTY_CATEGORY_FLAG:
                catalogue = raw_catalogues[catalogue_index]
                category = catalogue[self.__CATEGORIES_KEY][category_index]
                row_category = category[self.__NAME_KEY]
            else:
                row_category = None
            names.append(row_category)
        return names

    def __get_goals(self):
        return self.__raw_data[self.__METADATA_KEY][self.__GOALS_KEY]

    def __raise_not_a_variable_error(self, name):
        raise ValueError("'%s' is not a variable" % (name,))

    def __get_type_property(self, name):
        goals = self.__get_goals()
        for type_key in self.__ALL_VARIABLES_TYPES_KEYS:
            var_group = goals[type_key]
            if name in var_group:
                return self.__USER_TYPE_FOR_VARIABLE_TYPE_KEY[type_key]
        self.__raise_not_a_variable_error(name)

    def __get_bounds_property(self, name):
        input_var = self.__get_input_variable_or_throw(name)
        return input_var[self.__INPUT_LOWER_BOUND_KEY], input_var[self.__INPUT_UPPER_BOUND_KEY]

    def __get_all_variables(self):
        all_variables = dict()
        goals = self.__get_goals()
        for var_type_key in self.__ALL_VARIABLES_TYPES_KEYS:
            all_variables.update(goals[var_type_key])
        return all_variables

    def get_variables(self):
        """Returns the list of variables in the table."""
        return set(self.__get_all_variables())

    def get_catalogues(self):
        """Returns the list of catalogues in the table."""
        return set(self.__get_catalogue_names())

    def __get_variable(self, name):
        all_variables = self.__get_all_variables()
        if not name in all_variables:
            self.__raise_not_a_variable_error(name)
        return all_variables[name]

    def __get_vector_index_property(self, name):
        variable = self.__get_variable(name)
        if not variable[self.__IS_VECTOR_COMPONENT_PROPERTY_KEY]:
            return None
        else:
            return variable[self.__VECTOR_ID_PROPERTY_KEY]

    def __get_input_type_property(self, name):
        input_var = self.__get_input_variable_or_throw(name)
        try:
            return self.__INPUT_TYPES[input_var[self.__INPUT_TYPE_KEY]]
        except IndexError:
            raise ValueError("Unexpected type for input '%s'" % (name,))

    def __get_input_variable_or_throw(self, name):
        inputs = self.__get_goals()[self.__INPUTS_KEY]
        if not name in inputs:
            raise ValueError("'%s' is not an input variable" % (name,))
        return inputs[name]

    def get_variable_property(self, name, property):
        """Returns information about the specified variable, if available.

If the name is not associated to a variable, the function will raise a
ValueError.

Asking for a property unavailable for the specified variable will raise
a ValueError.

Valid properties are:

"type" - returns the type of the variable.

  It can be applied to all variables. It can return one of the following
  values: "input", "output", "objective", "constraint", "expression".

"bounds" - returns the lower and upper bound of a variable.

  It can be applied to input variables and returns a tuple with the
  lower and upper bounds of the variable.

"vector_index" - returns the index of a vector component, or None.

  It can be applied to all variables and returns the index of the specified
  vector component or 'None' for non-vector variables.

"default_value" - returns the default value.

  It can be applied to input variables and returns a float.

"input_type" - returns the type of the input variable.

  It can be applied to input variables and returns one of the following values:
  "variable", "constant", "expression" (the latter is only provided
  for compatibility reasons and will be deprecated).

"expression" - returns the expression of the variable.

  It can be applied to input variables, objectives, constraints and expressions and returns a string.

"limit" - returns the limit of a constraint.

  It can be applied to constraints and returns a float.

"tolerance" - returns the tolerance of a variable.

  It can be applied to input variables and constraints and returns a float.

"constraint_type" - returns the type of the constraint.

  It can be applied to constraints and returns one of the following values:
  "greater than", "equal to", "less than".

"objective_type" - returns the type of the objective.

  It can be applied to objectives and returns either "minimize" or "maximize".

"format" - returns the format of the variable.

  It can be applied to all types of variables and returns a string.

"description" - returns the description of the variable.

  It can be applied to all types of variables and returns a string.

"base" - returns the base of the input variable.

  It can be applied to input variables and returns an integer.

"step" - returns the step of the input variable.

  It can be applied to input variables and returns a float.

        """
        if not name in self.get_variables():
            raise ValueError("'%s' is not a variable" % (name,))
        if property == self.__TYPE_USER_PROPERTY:
            return self.__get_type_property(name)
        elif property == self.__BOUNDS_USER_PROPERTY:
            return self.__get_bounds_property(name)
        elif property == self.__VECTOR_INDEX_USER_PROPERTY:
            return self.__get_vector_index_property(name)
        elif property == self.__DEFAULT_VALUE_USER_PROPERTY:
            return self.__get_input_variable_or_throw(name)[self.__DEFAULT_VALUE_KEY]
        elif property == self.__INPUT_TYPE_USER_PROPERTY:
            return self.__get_input_type_property(name)
        elif property == self.__EXPRESSION_USER_PROPERTY:
            return self.__get_expression_property(name)
        elif property == self.__LIMIT_USER_PROPERTY:
            return self.__get_limit_property(name)
        elif property == self.__TOLERANCE_USER_PROPERTY:
            return self.__get_tolerance_property(name)
        elif property == self.__OBJECTIVE_TYPE_USER_PROPERTY:
            return self.__get_objective_type_property(name)
        elif property == self.__CONSTRAINT_TYPE_USER_PROPERTY:
            return self.__get_constraint_type_property(name)
        elif property == self.__FORMAT_USER_PROPERTY:
            return self.__get_variable(name)[self.__FORMAT_KEY]
        elif property == self.__DESCRIPTION_USER_PROPERTY:
            return self.__get_variable(name)[self.__DESCRIPTION_KEY]
        elif property == self.__BASE_USER_PROPERTY:
            return self.__get_input_variable_or_throw(name)[self.__BASE_KEY]
        elif property == self.__STEP_USER_PROPERTY:
            return self.__get_input_variable_or_throw(name)[self.__STEP_KEY]
        else:
            raise ValueError("'%s' is not a valid property" % (property,))

    def __get_expression_property(self, name):
        outputs = self.__get_goals()[self.__OUTPUTS_KEY]
        if name in outputs:
            raise ValueError("'%s' has to be an input variable, an objective or a constraint" % (name,))
        return self.__get_variable(name)[self.__EXPRESSION_KEY]

    def __get_limit_property(self, name):
        constraints = self.__get_goals()[self.__CONSTRAINTS_KEY]
        if not name in constraints:
            raise ValueError("'%s' is not a constraint" % (name,))
        return constraints[name][self.__LIMIT_KEY]

    def __get_tolerance_property(self, name):
        goals = self.__get_goals()
        vars = {**(goals[self.__CONSTRAINTS_KEY]), **(goals[self.__INPUTS_KEY])}
        if not name in vars:
            raise ValueError("'%s' is not an input variable or a constraint" % (name,))
        return vars[name][self.__TOLERANCE_KEY]

    def __get_constraint_type_property(self, name):
        constraints = self.__get_goals()[self.__CONSTRAINTS_KEY]
        if not name in constraints:
            raise ValueError("'%s' is not a constraint" % (name,))
        return self.__convert_constraint_type(constraints[name][self.__CONSTRAINT_TYPE_KEY], name)

    def __convert_constraint_type(self, type, name):
        try:
            return self.__CONSTRAINT_TYPES[type + 1]
        except IndexError:
            raise ValueError("Unexpected type for constraint '%s'" % (name,))

    def __get_objective_type_property(self, name):
        objectives = self.__get_goals()[self.__OBJECTIVES_KEY]
        if not name in objectives:
            raise ValueError("'%s' is not an objective" % (name,))
        return self.__convert_objective_type(objectives[name][self.__OBJECTIVE_TYPE_KEY], name)

    def __convert_objective_type(self, type, name):
        if type == 1:
            return self.__OBJECTIVE_TYPES[1]
        elif type == -1:
            return self.__OBJECTIVE_TYPES[0]
        else:
            raise ValueError("Unexpected type for objective '%s'" % (name,))

    def get_catalogue_property(self, catalogue_name, property):
        """Returns information about the categories of the specified catalogue.

Specifying an invalid property or catalogue will raise an Exception.

Valid values for 'property' are:

"names" - returns a set with the names of all categories in the catalogue.

"labels" - returns a dictionary with the labels associated with each category.

"titles" - returns a dictionary with the titles associated with each category.

"symbols" - returns a dictionary with the symbols associated with each category.

  Each symbol is represented by a dictionary with the following keys: 'shape',
  'color', 'fill_color', 'size', and 'border'.

  'shape' can be any of the shapes returned by the 'get_valid_shapes' method
  in the db.Shapes class."""
        catalogues = dict([(i[self.__CATALOGUE_NAME], i) for i in self.__raw_data[self.__METADATA_KEY][self.__CATALOGUES_KEY]])
        if catalogue_name not in catalogues:
            raise ValueError("'%s' is not a catalogue" % (catalogue_name,))
        categories = catalogues[catalogue_name][self.__CATEGORIES_KEY]
        if property == self.__CATALOGUE_LABELS_USER_PROPERTY:
            return self.__get_catalogue_properties(categories, self.__CATEGORY_LABEL)
        elif property == self.__CATALOGUE_NAMES_USER_PROPERTY:
            return set([i[self.__CATEGORY_NAME_KEY] for i in categories])
        elif property == self.__CATALOGUE_TITLES_USER_PROPERTY:
            return self.__get_catalogue_properties(categories, self.__CATEGORY_TITLE_KEY)
        elif property == self.__CATALOGUE_SYMBOLS_USER_PROPERTY:
            return self.__get_catalogue_symbols(categories)
        else:
            raise ValueError("'%s' is not a valid property" % (property,))

    def __get_catalogue_properties(self, categories, category_property_name, transform=lambda x: x):
        return dict([(category[self.__CATEGORY_NAME_KEY], transform(category[category_property_name]))
                     for category in categories])

    def __get_catalogue_symbols(self, categories):
        return self.__get_catalogue_properties(categories,
                                               self.__CATEGORY_SYMBOL_KEY,
                                               self.__symbol_converter.string_to_dict)

    def clone(self):
        """Returns a cloned table. The cloned table is not saved in modeFRONTIER"""
        if self.__is_robust() or self.__has_extra_ids():
            raise NotImplementedError("Cloning robust tables or their linked tables is not supported")

        cloned_table = DesignTable(self.__name, False, self.__show_robust_ids, False, True)
        cloned_table.__raw_data = self.__copy_raw_data()
        cloned_table.__linked_table = self.__linked_table.clone() if self.__linked_table else None
        return cloned_table

    def __copy_raw_data(self):
        data = {
            self.__NAME_KEY: self.__name,
            self.__METADATA_KEY: _copy.deepcopy(self.__raw_data[self.__METADATA_KEY]),
            self.__ROWS_KEY: _copy.copy(self.__raw_data[self.__ROWS_KEY])
        }
        return data

    def save(self, table_name=None):
        """For pyCONSOLE or pyFRONTIER saves the specified table in the Design Space.
        For CPython node saves the table to the specified DesignDB output parameter node.

        table_name
          For pyCONSOLE and pyFRONTIER optional parameter which, if specified, saves the table with the new name.
          For CPython node name of DesignDB output parameter node.
        """
        if self.__is_robust() or self.__has_extra_ids():
            raise NotImplementedError("Saving robust tables or their linked tables is not supported")

        encoder = _DesignTableEncoder(self.__raw_data, self.get_rows())
        builder = _EncodedHeaderTableBuilder(self.__get_save_name(table_name),
                                             encoder.get_encoded_column_names(),
                                             encoder.get_encoded_rows(),
                                             encoder.get_encoded_optional_properties())
        builder.check()
        return builder.build()

    def __get_save_name(self, table_name):
        if table_name is not None:
            _arg_parse.ensure_correct_args(("table_name", "string", table_name), )
            if len(table_name.strip()) == 0:
                raise ValueError("'table_name' can't be empty")
            return table_name
        else:
            return self.get_name()

    def insert(self, index, row):
        """Inserts a new row at the specified index."""
        if self.__is_robust() or self.__has_extra_ids():
            raise NotImplementedError("Changing robust tables or their linked tables is not supported")
        if not isinstance(index, int):
            raise TypeError("Invalid index type")
        header = self.__create_rows_header(self.__show_robust_ids)
        new_raw_row = self.__get_new_row(header, None, row)
        self.__raw_data[self.__ROWS_KEY].insert(index, new_raw_row)
        self.__id_cache.add(row[self.__PLAIN_TABLE_ID_INDEX])

    def sort(self, key=None, reverse=False):
        """Sorts the table rows in ascending or descending order
        using the specified comparator.

        key
          A function that returns a comparison key for a row.
          If not specified, the row ID is used as comparison key.
        reverse
          False by default. If True, sorts in descending order.
        """
        if self.__is_robust() or self.__has_extra_ids():
            raise NotImplementedError("Changing robust tables or their linked tables is not supported")
        if key is None:
            actual_key = lambda raw_row: raw_row[1][self.__ID_KEY]
        else:
            actual_key = lambda raw_row: key(self.__extract_row(raw_row, self.__create_plain_meta_columns))
        self.__raw_data[self.__ROWS_KEY].sort(key=actual_key, reverse=reverse)
