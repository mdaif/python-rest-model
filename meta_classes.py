from primitives import Typed
import requests
import json

def _post(self, **params):
    self.__dict__ = {}

    for k, v in params.items():
        setattr(self, k, v)

    body = json.dumps(self.__dict__)
    return requests.post(self.Meta.post, data=body)

def _put(self, id, **params):
    self.__dict__ = {}
    setattr(self, 'id', id)
    for k, v in params.items():
        setattr(self, k, v)

    body = json.dumps(self.__dict__)
    return requests.put(self.Meta.put, data=body)

def _delete(self, id):
    return requests.delete(self.Meta.delete)

def _get(self, id=None, **params):
    """if get has an id it should be used to retrieve a single item otherwise it would be retrieving a list"""

    self.__dict__ = {}
    if id is not None:
        setattr(self, 'id', id)
        # do some string interpolation to the endpoint
    for k, v in params.items():
        setattr(self, k, v)

    body = json.dumps(self.__dict__)
    return requests.put(self.Meta.get, data=body)




class RestModelMeta(type):
    def __new__(cls, clsname, bases, clsdict):
        for name, value in clsdict.items():
            if isinstance(value, Typed):
                value._name = name

        new_class = type.__new__(cls, clsname, bases, clsdict)

        setattr(new_class, "post", _post)
        setattr(new_class, "put", _put)
        setattr(new_class, "delete", _delete)
        setattr(new_class, "get", _get)

        return new_class
