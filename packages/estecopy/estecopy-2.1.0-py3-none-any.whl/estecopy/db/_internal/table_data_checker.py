
class __TableDataChecker:

    def _check_duplicated_columns(self, column_names):
        for index, column_name in enumerate(column_names, start=1):
            if not isinstance(column_name, str):
                raise TypeError("column %d is not a string" % (index,))
        names = set(column_names)
        if not len(names) == len(column_names):
            raise ValueError("column names should be unique")

    def _check_rows_length(self, column_names, rows):
        columns = len(column_names)
        for index, row in enumerate(rows, start=1):
            if not len(row) == columns:
                raise ValueError("row %d has %d columns (%d expected)" % (index, len(row), columns))
