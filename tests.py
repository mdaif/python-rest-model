from unittest.mock import patch
import models
import unittest
import json


class Stock(models.RestModel):
	name = models.StringField()
	shares = models.PositiveIntegerField()
	price = models.PositiveFloatField()

	class Meta:
		post = "http://www.mocky.io/v2/5185415ba171ea3a00704eed/"


class Student(models.RestModel):
	name = models.StringField()
	age = models.PositiveIntegerField()
	gpa = models.PositiveFloatField()

	class Meta:
		post = "http://www.mocky.io/v2/561a5fe6100000a32068d55f"
		put = "http://lalaland/students/{id}"
		delete = "http://www.mocky.io/v2/561a616f100000ef2068d561"
		get = "http://lalaland/classes/{class_id}/{student_id}"


class TestRestModelBehaviors(unittest.TestCase):
	@patch('requests.post')
	def test_post_1(self, post_mock):
		"""Happy path, all arguments are provided to post with correct data types"""
		stock = Stock()
		response = stock.post(name='EvilCorp', shares=3, price=2.2)
		self.assertTrue(post_mock.called)
		expected_data = {'name': 'EvilCorp', 'shares': 3, 'price': 2.2}
		post_mock.assert_called_with(Stock.Meta.post, data=json.dumps(expected_data))

	@patch('requests.post')
	def test_post_2(self, post_mock):
		"""Sad path, data type of an argument is not correct .. that should raise TypeError"""
		stock = Stock()
		with self.assertRaises(TypeError):
			stock.post(name='EvilCorp', shares=3, price="Very High")

		self.assertFalse(post_mock.called)


if __name__ == "__main__":
	unittest.main()
	# stock = Stock()
	# create_response = stock.post(name='EvilCorp', shares=3, price=2.2)
	# print(create_response.text)
	#
	# print("0", Student.__dict__)
	# student = Student()
	# print("1", student.__dict__)
	#
	# create_student = student.post(name='Daif', age=18, gpa=3.6)
	# print("2", student.__dict__)
	# print(create_student.json())
	#
	# update_student = student.format(id=10234).put(gpa=4.0)
	# print("3", student.__dict__)
	# print(update_student.json())
	#
	# get_student = student.get()
	# print("4", student.__dict__)
	# print(get_student.json())
	#
	# delete_student = student.format(id=10234).delete()
	# print("5", student.__dict__)
	# print(delete_student.status_code)
