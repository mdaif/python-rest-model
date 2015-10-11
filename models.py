from meta_classes import RestModelMeta
from primitives import Typed, Integer, Positive, String, Float


class RestModel(metaclass=RestModelMeta):
	pass


class PositiveIntegerField(Integer, Positive):
	pass


class PositiveFloatField(Float, Positive):
	pass


class StringField(String):
    pass
