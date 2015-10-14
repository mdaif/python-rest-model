from rest_client import models
from unittest.mock import patch
import unittest
import json



class Stock(models.RestModel):
    name = models.StringField()
    shares = models.PositiveIntegerField()
    price = models.PositiveFloatField()

    class Meta:
        post = "http://shangri-la/stocks/"
        put = "http://shangri-la/stocks/"
        delete = "http://shangri-la/stocks/delete"
        get = "http://shangri-la/stocks/"


class Student(models.RestModel):
    name = models.StringField()
    age = models.PositiveIntegerField()
    gpa = models.PositiveFloatField()

    class Meta:
        post = "http://shangri-la/students/"
        put = "http://shangri-la/students/{id}"
        delete = "http://shangri-la/students/{id}"
        get = "http://shangri-la/classes/{class_id}/{student_id}"


class TestRestModelBehaviors(unittest.TestCase):
    @patch('requests.post')
    def test_post_1(self, post_mock):
        """Happy path, all arguments are provided to post with correct data types"""
        stock = Stock()

        stock.format(json_body=True).post(name='EvilCorp', shares=3, price=2.2)
        self.assertTrue(post_mock.called)
        expected_data = {'name': 'EvilCorp', 'shares': 3, 'price': 2.2}

        # Testing json data is tricky because the order of the dict can change the solution is provided here
        # http://stackoverflow.com/a/28418085
        call_args, call_kwargs = post_mock.call_args
        self.assertEqual(call_args[0], Stock.Meta.post)
        self.assertIn('data', call_kwargs)
        self.assertDictEqual(json.loads(call_kwargs['data']), expected_data)

    @patch('requests.post')
    def test_post_2(self, post_mock):
        """Sad path, data type of an argument is not correct .. that should raise TypeError"""
        stock = Stock()
        with self.assertRaises(TypeError):
            stock.post(name='EvilCorp', shares=3, price="Very High")

        self.assertFalse(post_mock.called)

    @patch('requests.post')
    def test_post_1(self, post_mock):
        """Happy path, all arguments are provided to post with correct data types, parameters are sent as query
        string"""
        stock = Stock()
        stock.post(name='EvilCorp', shares=3, price=2.2)
        self.assertTrue(post_mock.called)
        expected_data = {'name': 'EvilCorp', 'shares': 3, 'price': 2.2}

        # Testing json data is tricky because the order of the dict can change the solution is provided
        # here http://stackoverflow.com/a/28418085
        call_args, call_kwargs = post_mock.call_args
        self.assertEqual(call_args[0], Stock.Meta.post)
        self.assertIn('data', call_kwargs)
        self.assertDictEqual(call_kwargs['data'], expected_data)

    @patch('requests.put')
    def test_put_1(self, put_mock):
        """Happy Path, the put endpoint should be formatted correctly """
        student = Student()
        student.format(id=18, json_body=True).put(name='Daif', age=27, gpa=3.6)
        self.assertTrue(put_mock.called)

        expected_data = {'name': 'Daif', 'age': 27, 'gpa': 3.6}

        call_args, call_kwargs = put_mock.call_args
        self.assertEqual(call_args[0], Student.Meta.put.format(id=18))  # notice the keyword formatting.
        self.assertIn('data', call_kwargs)
        self.assertDictEqual(json.loads(call_kwargs['data']), expected_data)

    @patch('requests.put')
    def test_put_2(self, put_mock):
        """Sad path, data type of an argument is not correct .. that should raise TypeError"""
        student = Student()
        with self.assertRaises(TypeError):
            student.format(id=18).put(name='Daif', age="twenty seven", gpa=3.6)

        self.assertFalse(put_mock.called)

    @patch('requests.put')
    def test_put_3(self, put_mock):
        """Happy Path, the put endpoint should be called correcly even if there is no format required """
        stock = Stock()
        stock.format(json_body=True).put(name='EvilCorp', shares=3, price=2.2)
        self.assertTrue(put_mock.called)

        expected_data = {'name': 'EvilCorp', 'shares': 3, 'price': 2.2}

        call_args, call_kwargs = put_mock.call_args
        self.assertEqual(call_args[0], Stock.Meta.put)  # notice the keyword formatting.
        self.assertIn('data', call_kwargs)
        self.assertDictEqual(json.loads(call_kwargs['data']), expected_data)

    @patch('requests.put')
    def test_put_4(self, put_mock):
        """Happy Path, the put endpoint should be formatted correctly, parameters are sent as query string. """
        student = Student()
        student.format(id=18).put(name='Daif', age=27, gpa=3.6)
        self.assertTrue(put_mock.called)

        expected_data = {'name': 'Daif', 'age': 27, 'gpa': 3.6}

        call_args, call_kwargs = put_mock.call_args
        self.assertEqual(call_args[0], Student.Meta.put.format(id=18))  # notice the keyword formatting.
        self.assertIn('data', call_kwargs)
        self.assertDictEqual(call_kwargs['data'], expected_data)

    @patch('requests.delete')
    def test_delete_1(self, delete_mock):
        """Happy Path, the delete endpoint should be formatted correctly """
        student = Student()
        student.format(json_body=True, id=18).delete(name='Daif', age=27, gpa=3.6)
        self.assertTrue(delete_mock.called)

        expected_data = {'name': 'Daif', 'age': 27, 'gpa': 3.6}

        call_args, call_kwargs = delete_mock.call_args
        self.assertEqual(call_args[0], Student.Meta.delete.format(id=18))  # notice the keyword formatting.
        self.assertIn('data', call_kwargs)
        self.assertDictEqual(json.loads(call_kwargs['data']), expected_data)

    @patch('requests.delete')
    def test_delete_2(self, delete_mock):
        """Sad path, data type of an argument is not correct .. that should raise TypeError"""
        student = Student()
        with self.assertRaises(TypeError):
            student.format(id=18).delete(name='Daif', age="twenty seven", gpa=3.6)

        self.assertFalse(delete_mock.called)

    @patch('requests.delete')
    def test_delete_3(self, delete_mock):
        """Happy Path, the delete endpoint should be called correcly even if there is no format required """
        stock = Stock()
        stock.format(json_body=True).delete(name='EvilCorp', shares=3, price=2.2)
        self.assertTrue(delete_mock.called)

        expected_data = {'name': 'EvilCorp', 'shares': 3, 'price': 2.2}

        call_args, call_kwargs = delete_mock.call_args
        self.assertEqual(call_args[0], Stock.Meta.delete)  # notice the keyword formatting.
        self.assertIn('data', call_kwargs)
        self.assertDictEqual(json.loads(call_kwargs['data']), expected_data)

    @patch('requests.delete')
    def test_delete_4(self, delete_mock):
        """Happy Path, the delete endpoint should be formatted correctly, parameters are sent as query string. """
        student = Student()
        student.format(id=18).delete(name='Daif', age=27, gpa=3.6)
        self.assertTrue(delete_mock.called)

        expected_data = {'name': 'Daif', 'age': 27, 'gpa': 3.6}

        call_args, call_kwargs = delete_mock.call_args
        self.assertEqual(call_args[0], Student.Meta.delete.format(id=18))  # notice the keyword formatting.
        self.assertIn('data', call_kwargs)
        self.assertDictEqual(call_kwargs['data'], expected_data)

    @patch('requests.get')
    def test_get_1(self, get_mock):
        """Happy Path, the get endpoint should be formatted correctly """
        student = Student()

        student.format(json_body=True, class_id=18, student_id=2).get(name='Daif', age=27, gpa=3.6)
        self.assertTrue(get_mock.called)

        expected_data = {'name': 'Daif', 'age': 27, 'gpa': 3.6}

        call_args, call_kwargs = get_mock.call_args
        self.assertEqual(call_args[0],
                         Student.Meta.get.format(class_id=18, student_id=2))  # notice the keyword formatting.
        self.assertIn('data', call_kwargs)
        self.assertDictEqual(json.loads(call_kwargs['data']), expected_data)

    @patch('requests.get')
    def test_get_2(self, get_mock):
        """Sad path, data type of an argument is not correct .. that should raise TypeError"""
        student = Student()
        with self.assertRaises(TypeError):
            student.format(json_body=True, class_id=18, student_id=2).get(name='Daif', age="twenty seven", gpa=3.6)

        self.assertFalse(get_mock.called)

    @patch('requests.get')
    def test_get_3(self, get_mock):
        """Happy Path, the get endpoint should be called correcly even if there is no format required """
        stock = Stock()
        stock.format(json_body=True).get(name='EvilCorp', shares=3, price=2.2)
        self.assertTrue(get_mock.called)

        expected_data = {'name': 'EvilCorp', 'shares': 3, 'price': 2.2}

        call_args, call_kwargs = get_mock.call_args
        self.assertEqual(call_args[0], Stock.Meta.get)  # notice the keyword formatting.
        self.assertIn('data', call_kwargs)
        self.assertDictEqual(json.loads(call_kwargs['data']), expected_data)

    @patch('requests.get')
    def test_get_4(self, get_mock):
        """Happy Path, the get endpoint should be formatted correctly, parameters are sent as query string """
        student = Student()

        student.format(class_id=18, student_id=2).get(name='Daif', age=27, gpa=3.6)
        self.assertTrue(get_mock.called)

        expected_data = {'name': 'Daif', 'age': 27, 'gpa': 3.6}

        call_args, call_kwargs = get_mock.call_args
        self.assertEqual(call_args[0],
                         Student.Meta.get.format(class_id=18, student_id=2))  # notice the keyword formatting.
        self.assertIn('data', call_kwargs)
        self.assertDictEqual(call_kwargs['data'], expected_data)

    def test_undefined_action(self):
        stock = Stock()
        with self.assertRaises(AttributeError):
            stock.head()


if __name__ == "__main__":
    unittest.main()
