from primitives import Typed
import requests
import json


class RestModelMeta(type):
    def _create(self, **params):
        for k, v in params.items():
            setattr(self, k, v)

        create_endpoint = self.Meta.create
        body = json.dumps(self.__dict__)
        return requests.post(create_endpoint, data=body)

    def _update(self, **params):
        self.__dict__ = {}
        for k, v in params.items():
            setattr(self, k, v)

        update_endpoint = self.Meta.update
        body = json.dumps(self.__dict__)
        return requests.put(update_endpoint, data=body)

    def __new__(cls, clsname, bases, clsdict):
        for name, value in clsdict.items():
            if isinstance(value, Typed):
                value._name = name

        new_class = type.__new__(cls, clsname, bases, clsdict)
        setattr(new_class, "create", cls._create)
        setattr(new_class, "update", cls._update)

        return new_class
