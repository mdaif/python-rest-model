from .meta_classes import RestModelMeta
from .primitives import Integer, Positive, String, Float, List


class RestModel(metaclass=RestModelMeta):
    """To be subclassed by the user's Models"""
    pass


class PositiveIntegerField(Integer, Positive):
    """Integer field with values >= 0"""
    pass


class PositiveFloatField(Float, Positive):
    """Float field with values >= 0.0 """
    pass


class StringField(String):
    """String Field"""
    pass


class IntegerField(Integer):
    """Integer Field"""
    pass


class FloatField(Float):
    """Float Field"""
    pass


class ListField(List):
    """List Field"""
    pass
