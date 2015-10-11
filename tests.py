import models


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
		put = "http://www.mocky.io/v2/561a604c100000a32068d560"
		delete = "http://www.mocky.io/v2/561a616f100000ef2068d561"
		get = "http://www.mocky.io/v2/561a5f0a100000872068d55e"


if __name__ == "__main__":
	stock = Stock()
	create_response = stock.post(name='IBM', shares=3, price=2.2)
	print(create_response.text)

	student = Student()
	print("1", student.__dict__)

	create_student = student.post(name='Daif', age=18, gpa=3.6)
	print("2", student.__dict__)
	print(create_student.json())

	update_student = student.put(10234, gpa=4.0)
	print("3", student.__dict__)
	print(update_student.json())

	get_student = student.get()
	print("4", student.__dict__)
	print(get_student.json())

	delete_student = student.delete(10234)
	print("5", student.__dict__)
	print(delete_student.status_code)
