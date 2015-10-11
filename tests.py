import models


class Stock(models.RestModel):
	name = models.StringField()
	shares = models.PositiveIntegerField()
	price = models.PositiveFloatField()

	class Meta:
		create = "http://www.mocky.io/v2/5185415ba171ea3a00704eed/"


class Student(models.RestModel):
	name = models.StringField()
	age = models.PositiveIntegerField()
	gpa = models.PositiveFloatField()

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
