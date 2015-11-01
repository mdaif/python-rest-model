"""Handle dynamic methods creation.

Meta Classes:
RestModelMeta -- create rest-model classes.
"""
from .primitives import Typed

import json
import requests


def _execute(self, verb, params):
    """Send requests to endpoint.

    verb -- the HTTP verb to be used (get, post, delete, ... etc)
    params -- the parameters to be passed in the HTTP request.
    """
    format_args = self.__dict__.pop(
        'format_args') if 'format_args' in self.__dict__ else None
    json_body = self.__dict__.pop(
        'json_body') if 'json_body' in self.__dict__ else None

    for k, v in params.items():
        setattr(self, k, v)

    if json_body:
        body = json.dumps(self.__dict__)
        headers = {'content-type': 'application/json'}
    else:
        body = self.__dict__.copy()
        headers = None

    endpoint = self.Meta.__dict__[verb].format(
        **format_args) if format_args else self.Meta.__dict__[verb]
    self.format_args = None
    self.json_body = None
    self.__dict__ = {}
    self.response = requests.__dict__[verb](endpoint, data=body,
                                            headers=headers)
    return self


def _format(self, json_body=False, **format_args):
    """Get endpoint format values.

    It caches the format values of endpoints and returns the same object.
    json_body -- boolean, if set to True all the parameters will be sent as
    JSON, otherwise the parameters will be sent as query string.
    format_args -- **kwargs, used to format the endpoint paths
    strings defined at the inner Meta class.
    """
    self.format_args = format_args
    self.json_body = json_body
    return self


class RestModelMeta(type):
    """Create RestModel classes."""

    def __new__(mcs, class_name, bases, class_dict):
        """Create a new RestModel class object.

        class_name -- name of class being created.
        bases -- bases of the class being created.
        class_dict -- instance variables.
        """
        for name, value in class_dict.items():
            if isinstance(value, Typed):
                value._name = name

        new_class = type.__new__(mcs, class_name, bases, class_dict)

        if class_name != "RestModel":  # not the base class
            # An inner Meta class must be provided,
            # otherwise the model is meaningless !
            if 'Meta' not in class_dict:
                raise Exception("Meta class must be provided")

            # attach functions and attributes to the RestModel classes.
            setattr(new_class, "format_args", None)
            setattr(new_class, "json_body", None)
            setattr(new_class, "format", _format)
            setattr(new_class, '_execute', _execute)

            verbs = [x for x, y in class_dict['Meta'].__dict__.items() if
                     type(y) == str and not x.startswith(
                         "__")]
            # dynamically extracts the HTTP endpoints defined
            # in the inner Meta class.

            method_definition = """
def _{0}(self, **params):
    return self._execute('{0}', params)
            """  # for each endpoint define a wrapper method
            # called _{verb_name}. This method will be passed the
            # parameters to be sent in the HTTP query.
            for verb in verbs:
                supported_verb = method_definition.format(verb)
                exec (supported_verb)  # create the method.
                setattr(new_class, verb, locals()[
                    "_" + verb])  # attach the method to the class object.

        return new_class
