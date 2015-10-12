from primitives import Typed
from types import MethodType, FunctionType
import requests
import json


def _execute(self, verb, params):
    format_args = self.__dict__.pop('format_args') if 'format_args' in self.__dict__ else None
    json_body = self.__dict__.pop('json_body') if 'json_body' in self.__dict__ else None

    for k, v in params.items():
        setattr(self, k, v)

    if json_body:
        body = json.dumps(self.__dict__)
        headers = {'content-type': 'application/json'}
    else:
        body = self.__dict__.copy()
        headers = None

    endpoint = self.Meta.__dict__[verb].format(**format_args) if format_args else self.Meta.__dict__[verb]
    self.format_args = None # this should be handled in a cleaner way
    self.json_body = None
    self.__dict__ = {}
    return requests.__dict__[verb](endpoint, data=body, headers=headers)


def _format(self, json_body=False, **format_args):
    self.format_args = format_args
    self.json_body = json_body
    return self


class RestModelMeta(type):
    def __new__(cls, clsname, bases, clsdict):
        for name, value in clsdict.items():
            if isinstance(value, Typed):
                value._name = name

        new_class = type.__new__(cls, clsname, bases, clsdict)

        if clsname != "RestModel":
            if 'Meta' not in clsdict:
                raise Exception("Meta class must be provided")

            setattr(new_class, "format_args", None)
            setattr(new_class, "json_body", None)
            setattr(new_class, "format", _format)
            setattr(new_class, '_execute', _execute)

            verbs = [x for x,y in clsdict['Meta'].__dict__.items() if type(y) == str and not x.startswith("__")]

            method_definition = """
def _{0}(self, **params):
    self._execute('{0}', params)
            """
            for verb in verbs:
                supported_verb = method_definition.format(verb)
                exec(supported_verb)
                setattr(new_class, verb, locals()["_" + verb])

        return new_class
