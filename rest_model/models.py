"""Contain Fields to be used by user code."""
try:
    from .meta_classes import RestModelMeta
    from .primitives import Integer, Positive, String, Float, List
except SystemError:
    from meta_classes import RestModelMeta
    from primitives import Integer, Positive, String, Float, List


class RestModel(metaclass=RestModelMeta):
    """Be a superclass to the user Models."""

    pass


class PositiveIntegerField(Integer, Positive):
    """Create Integer field with values >= 0."""

    pass


class PositiveFloatField(Float, Positive):
    """Create Float field with values >= 0.0 ."""

    pass


class StringField(String):
    """Create String Field."""

    pass


class IntegerField(Integer):
    """Create Integer Field."""

    pass


class FloatField(Float):
    """Create Float Field."""

    pass


class ListField(List):
    """Create List Field."""

    pass
