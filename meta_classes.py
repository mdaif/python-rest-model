from primitives import Typed
from types import MethodType, FunctionType
import requests
import json


def _execute(self, verb, params):
    format_args = self.__dict__.pop('format_args') if 'format_args' in self.__dict__ else None

    for k, v in params.items():
        setattr(self, k, v)

    body = json.dumps(self.__dict__)
    endpoint = self.Meta.__dict__[verb].format(**format_args) if format_args else self.Meta.__dict__[verb]
    self.format_args = None # this should be handled in a cleaner way
    self.__dict__ = {}
    return requests.__dict__[verb](endpoint, data=body)


def _format(self, **format_args):
    self.format_args = format_args
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
