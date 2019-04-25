import requests
import inspect


class AsDictObject:
    def as_dict(self):
        attributes = inspect.getmembers(self, lambda a: not inspect.isroutine(a))
        dict_repr = {}
        for name, value in attributes:
            if '_' not in name[0]:
                if isinstance(value, AsDictObject):
                    value = value.as_dict()
                elif isinstance(value, list):
                    value = [i.as_dict() if isinstance(i, AsDictObject) else i for i in value]
                dict_repr[name] = value
        return dict_repr


class GenericAPIConnector:
    @property
    def base_api_url(self):
        raise NotImplementedError()

    base_data = {}
    base_header = {}

    @property
    def resource_config(self):
        raise NotImplementedError()


class UserObject(AsDictObject):
    name = 'test'

class ImplementedAPIConnector(GenericAPIConnector):

    base_api_url = 'http://127.0.0.1:8000/'
    resource_config = {
        'users': {
            'methods': ('create', 'retrieve', 'update', 'destroy', 'list'),
            'data_obj': {
                'name': {'required': True}
            }
            # 'subresources': ('posboxes') or define it anew, but not going to implement this for now
        },
        'postboxes': {
            'methods': ('create',)
        }
    }


test = ImplementedAPIConnector()
print(test.base_api_url)
