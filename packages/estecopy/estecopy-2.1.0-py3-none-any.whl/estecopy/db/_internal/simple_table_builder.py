from estecopy.db._internal import attributes as _attributes
from estecopy.db._internal.encoded_header_table_builder import _EncodedHeaderTableBuilder
from estecopy.db._internal.table_data_checker import __TableDataChecker


class __SimpleTableBuilder(__TableDataChecker):
    __INPUT_COLUMN_PREFIX = _attributes.INPUT_COLUMN_PREFIX
    __OUTPUT_COLUMN_PREFIX = _attributes.OUTPUT_COLUMN_PREFIX

    def __init__(self, table_name, column_names, rows, optional_properties=None):
        self.table_name = table_name
        self.column_names = column_names
        self.rows = rows
        self.optional_properties = optional_properties

    def check(self):
        self._check_duplicated_columns(self.column_names)
        self._check_rows_length(self.column_names, self.rows)

    def build_input_table(self):
        return self.__build_with_prefix(self.__INPUT_COLUMN_PREFIX)

    def build_output_table(self):
        return self.__build_with_prefix(self.__OUTPUT_COLUMN_PREFIX)

    def __build_with_prefix(self, prefix):
        builder = _EncodedHeaderTableBuilder(self.table_name, [prefix + i for i in self.column_names], self.rows, self.optional_properties)
        builder.check()
        return builder.build()
