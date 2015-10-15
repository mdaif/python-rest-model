Introduction
============

Python Rest Client exists to solve the common problem of consuming
RESTful services.

The Problem
===========

In an OOP language as Python, developers tend to think of their data as
objects and associated attributes and behaviors. When it comes to
consuming a RESTful service, you typically wrap the actual communication
using functions, methods or classes and spend some time to design your
handler(s). That typically results in repetitive and not-so-readable
code. Also different developers usually have different approaches on how
to handle this issue. If you want to make sure you are passing the right
data types that would be a totally different story !

The Solution
============

Python Rest Client solves these issues by treating the RESTful endpoints
as they should be ... endpoints to resources ! It lets you define your
own resources like you do in Django models, by extending a class and
defining some attributes, and that's it ! You can have objects that
handles data type validation on attributes, define the endpoints once at
a single location, and the operations can be chained.

Quick Start
===========

After you install Python Rest Client you can use it as following.

::

        from rest_client import models         # import models
        
        class Student(models.RestModel):       # extend models.RestModel
          name = models.StringField()
          age = models.PositiveIntegerField()
          gpa = models.PositiveFloatField()

          class Meta:             # An inner meta class is required to define endpoints
            post = "http://shangri-la/students/"  # each entry should map to an HTTP action
            put = "http://shangri-la/students/{id}"
            delete = "http://shangri-la/students/{id}"
            get = "http://shangri-la/classes/{class_id}/{student_id}"

After you define your resource and the endpoints you need, you can use
them as following ...

::

        student = Student()
        student.post(name='Bob', age=27, gpa=3.6)

If you try to assign an attribute a wrong data type a TypeError will be
raised

::

        >>> student.post(name=7, age=27, gpa=3.6)

::

        Traceback (most recent call last):
        ...
        TypeError: expected <class 'str'>

You can format the endpoints at each request using the format method,
which makes it very easy to follow the DRY principle and at the same
time dealing with multiple resources of the same type based on a
different id. For example if you need to get students with ids in range
13 to 20 at a class with id 15 you can do the following ...

::

        for i in range(13, 21):
          student = student.format(class_id=15, student_id=i).get()
          response = student.response

each returned object from get, post, ...etc methods is a requests
response object: http://docs.python-requests.org/en/latest/

The attributes are sent as query string unless you set the json\_body
argument at format method to be True, they will be sent as JSON body
with the proper header.

::

        student.format(json_body=True, id=18).put(name='Alice', age=27, gpa=3.6)

the post, put, ... etc methods used in the examples are dynamically
generated based on what you define in the inner Meta class, if you try
to call an undefined action an AttributeError will be raised. You can
find additional examples in the tests directory.

Currently supported data types
==============================

-  StringField
-  IntegerField
-  FloatField
-  ListField
-  PositiveIntegerField
-  PositiveFloatField

