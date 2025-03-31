from estecopy._internal import _db
from estecopy._utils import arg_parse as _arg_parse
from estecopy.db._internal.attributes import *
from estecopy.db._internal.design_table import DesignTable
from estecopy.db._internal.encoded_header_table_builder import _EncodedHeaderTableBuilder
from estecopy.db._internal.shapes import *
from estecopy.db._internal.simple_table_builder import __SimpleTableBuilder

__ALL_TABLES = "all"

def get_version():
    """Returns the version of this module as (major, minor, patch)."""
    return 1, 3, 0


def get_table_names():
    """Returns names of the available tables."""
    if __ALL_TABLES not in _db.get_table_types():
        return ()
    else:
        return _db.get_table_names(__ALL_TABLES)


def create_table(table_name, encoded_column_names, rows, optional_properties=None,
                 objectives=None, constraints=None, expressions=None):
    """Creates table in Design Space.

table_name
  name of the new table. Duplicated names are not allowed.
encoded_column_names
  variable type encoding followed by variable name (see example
  below). Columns require different value formats based on their type:


  Name        Description       Format
  ==================================================
  id          design ID         non-negative integer
  marked      "mark" status     boolean
  virtual     "virtual" status  boolean
  cat:<name>  a catalogue       string
  in:<name>   input variable    scalar
  out:<name>  output variable   scalar

rows
  list of values in the format required by the corresponding column
  type (see column encoding above). Each row is a design. Number of
  values in a row has to correspond to the number of columns.

optional_properties
  dictionary with optional properties to add to the table.

  There are two kind of properties: variable properties and catalogue
  properties.

  Valid variable properties are:

    Name             Description           Format
    ==========================================================
    bounds           variable bounds       list of two scalars
    default_value    default value         scalar
    type             variable type         string
      variable   (optional)
      constant   (requires 'default_value' key)
    base             variable base         integer
    format           variable format       string
    description      variable description  string

  Valid catalogue properties are:

    Name          Description          Format
    ===================================================
    label        category label        string
    size         symbol size           scalar
    border       symbol border width   scalar
    shape        symbol shape          any shape declared in db.Shapes
    color        symbol border color   RGB/RGBA or HEX string
    fill_color   symbol fill color     RGB/RGBA or HEX string

objectives
  dictionary with the objectives to add to the table.

  Valid objective properties are:

    Name          Description            Format
    ==================================================
    type          objective type         'maximize' or 'minimize'
    expression    objective expression   string
    format        objective format       string
    description   objective description  string

constraints
  dictionary with the constraints to add to the table.

  Valid constraint properties are:

    Name          Description             Format
    ==================================================
    type          constraint type         'less than', 'equal to'
                                            or 'greater than'
    tolerance     constraint tolerance    double
    limit         constraint limit        double
    expression    constraint expression   string
    format        constraint format       string
    description   constraint description  string

expressions
  dictionary with the expressions to add to the table.

  Valid expression properties are:

    Name          Description             Format
    ==================================================
    expression    expression expression   string
    format        expression format       string
    description   expression description  string

Example:

from estecopy import db
from estecopy.db import Shapes

objectives = {"obj1": {"type": "maximize", "expression": "input1", "format": "%2.5g", "description": "objective"},
              "obj2": {"type": "minimize", "expression": "input1 + output1"}}
constraints = {"const1": {"type": "less than", "tolerance": 16.0, "limit": 7.0, "expression": "input1 + input2", "format": "%2g", "description": "constraint"},
               "const2": {"type": "greater than", "tolerance": 167.0, "limit": 78.0, "expression": "output1 + output2"},
               "const3": {"type": "equal to", "tolerance": 67.0, "limit": -12.0, "expression": "output1 - output2", "format": "%5g"}}
expressions = {"expr1": {"expression": "output1"},
               "expr2": {"expression": "input1 - output1", "format": "%2g", "description": "expression"}}

db.create_table('my_table',
        ['id', 'cat:color', 'in:input1', 'in:input2', 'out:output1', 'out:output2', 'marked'],
        [[3,   'red',        1.3,         1,           0.9,           -1.3,          True],
         [5,   'red',        2,           2,           1.5,           2.3,           False],
         [6,   'blue',       3.6,         3,           0.1,           -2,            False],
         [7,   'green',      4.1,         4,           3.2,           1,             True]],
         {"input1": {"type": "constant", "default_value": 12, "base": 1, "format": "%g", "description": "input"},
          "output1": {"format": "%g", "description": "output"},
          "color": {"red" : {
                             "shape" : Shapes.SQUARE,
                             "color" : "#FF0000",
                             "fill_color" : "#ff8888",
                             "size" : 15,
                             "border" : 2
                            },
                    "green" : {
                             "label" : "GR",
                             "fill_color" : "#88ff88",
                            }}},
          objectives=objectives, constraints=constraints, expressions=expressions)

creates a table called my_table with 1 catalogue, 2 input variables, 2 output variables,
2 objectives, 3 constraints, 2 expressions and 4 designs. The ID sequence is custom.
The first and the last designs are marked.

    """
    builder = _EncodedHeaderTableBuilder(table_name, encoded_column_names, rows, optional_properties,
                                         objectives, constraints, expressions)
    builder.check()
    return builder.build()


def create_input_table(table_name, column_names, rows, optional_properties=None):
    """Creates table with only input variables in Design Space.

table_name
  name of the new table. Duplicated names are not allowed.

column_names
  list of input names in string format

rows
  a row (design) consists of a list/tuple of values, where each value
  is the value of this design in a variable. Number of values in a row
  has to correspond to the number of columns.

optional_properties
  dictionary with optional properties to add to the table.
  See description for method create_table.

Returns the name of the new table.

Example:

from estecopy import db

db.create_input_table("input_table",
                       ["x1", "x2"],
                       [[1, 2], [2, 4], [3, 6], [4, 8]],
                       {"x2":{"bounds" : [-10,10], "default_value": 10},
                       "x1": {"type": "constant", "default_value": 12, "base": 1, "format": "%h", "description": "input"}})
    """
    builder = __SimpleTableBuilder(table_name, column_names, rows, optional_properties)
    builder.check()
    return builder.build_input_table()


def create_output_table(table_name, column_names, rows, optional_properties=None):
    """Creates table with only output variables in Design Space.

See description for method create_input_table.

Example:

from estecopy import db

db.create_output_table("output_table",
                        ["f1", "f2"],
                        [[1, 2], [2, 4], [3, 6], [4, 8]],
                        {"f2": {"format": "%h"},
                        "f1": {"format": "%f", "description": "output1"}})
"""
    builder = __SimpleTableBuilder(table_name, column_names, rows, optional_properties)
    builder.check()
    return builder.build_output_table()


def get_table(name, show_progress=True, show_robust_ids=False, preload_linked_table=True):
    """Returns a table of class 'DesignTable'

show_progress: print the progress of table loading
show_robust_ids: for robust and design tables, show the RIDs or the associated IDs of the designs, if present
preload_linked_table: for robust tables only, load the robust table and the associated design table

Lazy loading with 'preload_linked_table=False' should be used with
caution, as it may cause errors if the model is renamed in
modeFRONTIER.

    """
    _arg_parse.ensure_correct_args(("name", "string", name), )
    return DesignTable(name, show_progress, show_robust_ids, preload_linked_table)


__all__ = sorted(["get_version", "get_table_names", "create_table", "create_input_table", "create_output_table", "get_table", "DesignTable",
                  "Shapes"])
