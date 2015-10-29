try:
    from .primitives import Typed
except SystemError:
    from primitives import Typed
import json
import requests


def _execute(self, verb, params):
    """ Wrapped by the generated action method (like _get, _post ... etc). It is responsible for the actual formatting
    of the endpoint params, and passing values.
    verb -- the HTTP verb to be used (get, post, delete, ... etc)
    params -- the parameters to be passed in the HTTP request."""

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
    self.format_args = None  # this should be handled in a cleaner way
    self.json_body = None
    self.__dict__ = {}
    self.response = requests.__dict__[verb](endpoint, data=body, headers=headers)
    return self


def _format(self, json_body=False, **format_args):
    """ Responsible for defining the attribute sending behavior. And getting the endpoint format values.
    json_body -- boolean, if set to True all the parameters will be sent as JSON, otherweise the paremeters will be
    sent as query string.
    format_args -- **kwargs, used to format the endpoint paths strings defined at the inner Meta class.
    returns the same object.
    """
    self.format_args = format_args
    self.json_body = json_body
    return self


class RestModelMeta(type):
    """ A metaclass that is responsible for creating RestModel classes"""

    def __new__(cls, clsname, bases, clsdict):
        for name, value in clsdict.items():
            if isinstance(value, Typed):
                value._name = name

        new_class = type.__new__(cls, clsname, bases, clsdict)

        if clsname != "RestModel":
            if 'Meta' not in clsdict:  # An inner Meta class must be provided, othwerise the model is meaningless !
                raise Exception("Meta class must be provided")

            # attach functions and attributes to the RestModel classes.
            setattr(new_class, "format_args", None)
            setattr(new_class, "json_body", None)
            setattr(new_class, "format", _format)
            setattr(new_class, '_execute', _execute)

            verbs = [x for x, y in clsdict['Meta'].__dict__.items() if type(y) == str and not x.startswith(
                "__")]  # dynamically extracts the HTTP endpoints defined in the inner Meta class.

            method_definition = """
def _{0}(self, **params):
    return self._execute('{0}', params)
            """  # for each endpoint define a wrapper method called _verb_name. This method will be passed the
            # parameters to be sent in the HTTP query.
            for verb in verbs:
                supported_verb = method_definition.format(verb)
                exec(supported_verb)  # create the method.
                setattr(new_class, verb, locals()["_" + verb])  # attach the method to the class object.

        return new_class
