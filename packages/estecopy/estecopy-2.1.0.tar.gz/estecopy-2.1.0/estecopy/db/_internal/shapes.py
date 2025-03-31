
class Shapes:
    SQUARE = "SQUARE"
    DIAMOND = "DIAMOND"
    TRIANGLE = "TRIANGLE"
    TRIANGLE_DOWN = "TRIANGLE_DOWN"
    CIRCLE = "CIRCLE"
    CROSS = "CROSS"
    X = "X"
    H_LINE = "H_LINE"
    V_LINE = "V_LINE"
    STAR = "STAR"
    NONE = "NONE"

    __valid_shapes = None

    @staticmethod
    def get_valid_shapes():
        Shapes.__valid_shapes = Shapes.__valid_shapes or set([getattr(Shapes, i) for i in dir(Shapes) if i.upper() == i])
        return set(Shapes.__valid_shapes)

    @staticmethod
    def is_valid_shape(string):
        Shapes.__valid_shapes = Shapes.__valid_shapes or set([getattr(Shapes, i) for i in dir(Shapes) if i.upper() == i])
        return string in Shapes.__valid_shapes
