from estecopy.db._internal import attributes as _attributes
from estecopy.db._internal.shapes import Shapes as _Shapes


class _SymbolConverter:
    __CommonTableAttributes = _attributes._CommonTableAttributes

    __CATEGORY_SYMBOL_SHAPE = __CommonTableAttributes._CATEGORY_SYMBOL_SHAPE
    __CATEGORY_SYMBOL_SIZE = __CommonTableAttributes._CATEGORY_SYMBOL_SIZE
    __CATEGORY_SYMBOL_COLOR = __CommonTableAttributes._CATEGORY_SYMBOL_COLOR
    __CATEGORY_SYMBOL_BORDER = __CommonTableAttributes._CATEGORY_SYMBOL_BORDER
    __CATEGORY_SYMBOL_FILL_COLOR = __CommonTableAttributes._CATEGORY_SYMBOL_FILL_COLOR

    __DEFAULT_SHAPE = "CIRCLE"
    __DEFAULT_SIZE = 11
    __DEFAULT_COLOR = "#000000"
    __DEFAULT_BORDER = 1
    __DEFAULT_FILL_COLOR = None

    def __init__(self):
        pass

    def string_to_dict(self, string_representation):
        fields = string_representation.split(",")
        del (fields[1])  # don't expose the LINE field of the Symbol to the user
        fields[1] = int(fields[1])
        fields[3] = int(fields[3])
        result = dict(zip((self.__CATEGORY_SYMBOL_SHAPE,
                           self.__CATEGORY_SYMBOL_SIZE,
                           self.__CATEGORY_SYMBOL_COLOR,
                           self.__CATEGORY_SYMBOL_BORDER,
                           self.__CATEGORY_SYMBOL_FILL_COLOR),
                          fields))
        if self.__CATEGORY_SYMBOL_FILL_COLOR not in result:
            result[self.__CATEGORY_SYMBOL_FILL_COLOR] = None
        return result

    def dict_to_string(self, dict_representation):
        shape = self.__ensure_shape(dict_representation.get(self.__CATEGORY_SYMBOL_SHAPE, None) or self.__DEFAULT_SHAPE)
        size = self.__ensure_number("size", dict_representation.get(self.__CATEGORY_SYMBOL_SIZE, None) or self.__DEFAULT_SIZE)
        color = self.__convert_color(dict_representation.get(self.__CATEGORY_SYMBOL_COLOR, None) or self.__DEFAULT_COLOR)
        border = self.__ensure_number("border", dict_representation.get(self.__CATEGORY_SYMBOL_BORDER, None) or self.__DEFAULT_BORDER)
        raw_fill_color = dict_representation.get(self.__CATEGORY_SYMBOL_FILL_COLOR, None) or self.__DEFAULT_FILL_COLOR
        if raw_fill_color:
            fill_color = self.__convert_color(raw_fill_color)
            return "%s,NONE,%s,%s,%s,%s" % (shape, size, color, border, fill_color)
        else:
            return "%s,NONE,%s,%s,%s" % (shape, size, color, border)

    def __ensure_shape(self, user_definition):
        if _Shapes.is_valid_shape(user_definition):
            return user_definition
        else:
            message = "Invalid shape definition: '%s'" % (user_definition,)
            raise ValueError(message)

    def __ensure_number(self, field_name, user_definition):
        try:
            return max(0, int(user_definition))
        except:
            message = "Invalid %s definition: '%s'" % (field_name, user_definition)
            raise ValueError(message) from None

    def __convert_color(self, user_definition):
        if isinstance(user_definition, str):
            return self.__ensure_css_color(user_definition)
        else:
            try:
                return self.__color_to_CSS_color(user_definition)
            except:
                message = "Invalid color definition: '%s'" % (user_definition,)
                raise ValueError(message) from None

    def __ensure_css_color(self, user_definition):
        length = len(user_definition)
        if user_definition.startswith("#") and (length == 7 or length == 9):
            return user_definition
        else:
            raise ValueError("Invalid color definition: '%s'" % (user_definition,))

    def __color_to_CSS_color(self, rgb):
        clipped_components = [min(255, max(0, i)) for i in rgb]
        if len(clipped_components) == 3:
            format_string = "#{:02x}{:02x}{:02x}"
        else:
            format_string = "#{:02x}{:02x}{:02x}{:02x}"
        return format_string.format(*clipped_components)
