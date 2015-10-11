class Typed:
	_expected_type = type(None)

	def __init__(self, name=None):
		self._name = name

	def __set__(self, instance, value):
		if not isinstance(value, self._expected_type):
			raise TypeError('Expected ' + str(self._expected_type))
		instance.__dict__[self._name] = value


class Integer(Typed):
	_expected_type = int


class Float(Typed):
	_expected_type = float


class String(Typed):
	_expected_type = str


class Positive(Typed):
	def __set__(self, instance, value):
		if value < 0:
			raise TypeError("Expected value to be >= 0")
		super().__set__(instance, value)
