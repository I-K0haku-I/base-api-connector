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

    def __new__(cls):
        for resource, settings in cls.resource_config.items():
            for setting, content in settings.items():
                # TODO: rename methods to something else so it's distinct to get etc.
                if setting == 'methods':
                    for method in content:
                        print(f'{resource}_{method}')
                        # TODO: why are the created attributes all the same function??? They all return the latest resource+method
                        setattr(cls, f'{resource}_{method}', lambda self, *a, **kw: self.create_attr(resource, method, *a, **kw))
        return object.__new__(cls)
    
    singular_methods = ('retrieve', 'update', 'destroy')

    def create_attr(self, resource, method, *args, **kwargs):
        print(resource)
        url = f'{self.base_api_url}{resource}/'
        if method in self.singular_methods:
            pk = args[0]
            url += str(pk)
        print(url)

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
            'methods': ('retrieve',)
        }
    }


conn = ImplementedAPIConnector()
conn.users_retrieve(1)