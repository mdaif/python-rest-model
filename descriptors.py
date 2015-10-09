import requests
import json


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
			raise TypeError("Expected value > 0")
		super().__set__(instance, value)

class PositiveInteger(Integer, Positive):
	pass

class PositiveFloat(Float, Positive):
	pass


class HttpModelMeta(type):
	def _create(self, **params):
		for k, v in params.items():
			setattr(self, k, v)

		create_endpoint = self.Meta.create
		body = json.dumps(self.__dict__)
		return requests.post(create_endpoint, data=body)

	def _update(self, **params):
		self.__dict__ = {}
		for k, v in params.items():
			setattr(self, k, v)

		update_endpoint = self.Meta.update
		body = json.dumps(self.__dict__)
		return requests.put(update_endpoint, data=body)

	def __new__(cls, clsname, bases, clsdict):
		for name, value in clsdict.items():
			if isinstance(value, Typed):
				value._name = name

		new_class = type.__new__(cls, clsname, bases, clsdict)
		setattr(new_class, "create", cls._create)
		setattr(new_class, "update", cls._update)
		return new_class

class HttpModel(metaclass=HttpModelMeta):
	pass


class Stock(HttpModel):
	name = String()
	shares = PositiveInteger()
	price = PositiveFloat()

	class Meta:
		create = "http://www.mocky.io/v2/5185415ba171ea3a00704eed/"

class Student(HttpModel):
	name = String()
	age = PositiveInteger()
	gpa = PositiveFloat()

	class Meta:
		create = "http://www.mocky.io/v2/5617b761100000132472226c"
		update = "http://www.mocky.io/v2/5617b761100000132472226c"

if __name__ == "__main__":
	stock = Stock()
	create_response = stock.create(name='daif', shares=3, price=2.2)
	print(create_response.text)

	student = Student()
	print("1", student.__dict__)
	create_student = student.create(name='7amada', age=18, gpa=3.6)
	print("2", student.__dict__)
	print(create_student.json())

	update_student = student.update(name='7amboozo', age=19)
	print("3", student.__dict__)
	print(update_student.json())
