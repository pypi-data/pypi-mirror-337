METADATA_KEY = "metadata"
INPUTS_KEY = "inputs"
OUTPUTS_KEY = "outputs"
CATEGORIES_KEY = "categories"
DATA_KEY = "data"
COLUMN_NAMES_KEY = "column_names"
MARKED_KEY = "marked"
LINKED_SESSION_TABLE_NAME_KEY = "linked_session_table_name"

NAME_KEY = "name"
ROWS_KEY = "rows"
ID_KEY = "id"
RID_KEY = "rid"
IDS_KEY = "ids"
VIRTUAL_KEY = "virtual"

ID_COLUMN_NAME = ID_KEY
MARKED_COLUMN_NAME = MARKED_KEY
VIRTUAL_COLUMN_NAME = VIRTUAL_KEY
CATALOGUE_COLUMN_PREFIX = "cat:"
INPUT_COLUMN_PREFIX = "in:"
OUTPUT_COLUMN_PREFIX = "out:"


class _CommonTableAttributes:
    _TYPE_KEY = "type"
    _DEFAULT_VALUE_KEY = "default_value"
    _BASE_KEY = "base"
    _FORMAT_KEY = "format"
    _DESCRIPTION_KEY = "description"
    _CATEGORY_LABEL = "label"
    _CATEGORY_SYMBOL_SHAPE = "shape"
    _CATEGORY_SYMBOL_SIZE = "size"
    _CATEGORY_SYMBOL_COLOR = "color"
    _CATEGORY_SYMBOL_BORDER = "border"
    _CATEGORY_SYMBOL_FILL_COLOR = "fill_color"
    _EXPRESSION_KEY = "expression"
    _TOLERANCE_KEY = "tolerance"
    _LIMIT_KEY = "limit"
    _OBJECTIVES_KEY = "objectives"
    _OBJECTIVE_TYPES = ("minimize", "maximize")
    _CONSTRAINTS_KEY = "constraints"
    _CONSTRAINT_TYPES = ("greater than", "equal to", "less than")

__all__ = sorted(['CATEGORIES_KEY', 'CATALOGUE_COLUMN_PREFIX', 'COLUMN_NAMES_KEY', 'DATA_KEY',
           'IDS_KEY', 'ID_COLUMN_NAME', 'ID_KEY', 'INPUTS_KEY', 'INPUT_COLUMN_PREFIX',
           'LINKED_SESSION_TABLE_NAME_KEY', 'MARKED_COLUMN_NAME', 'MARKED_KEY', 'METADATA_KEY',
           'NAME_KEY', 'OUTPUTS_KEY', 'OUTPUT_COLUMN_PREFIX', 'RID_KEY', 'ROWS_KEY',
           'VIRTUAL_COLUMN_NAME', 'VIRTUAL_KEY'])