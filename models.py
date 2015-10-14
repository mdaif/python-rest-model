from meta_classes import RestModelMeta
from primitives import Typed, Integer, Positive, String, Float


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
