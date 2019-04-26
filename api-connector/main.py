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
                if setting == 'commands':
                    for command in content: # TODO: maybe make multiple lambdas depending on command or some magic stuff
                        setattr(cls, f'{resource}_{command}', lambda self, *a, resource=resource, command=command, **kw: self.create_attr(resource, command, *a, **kw))
                # if setting == 'data':
        
        cls.commands_to_methods = dict(zip(cls.possible_commands, cls.corresponding_methods))


        return object.__new__(cls)
    
    possible_commands = ('list', 'create', 'retrieve', 'update', 'destroy')
    corresponding_methods = ('get', 'post', 'get', 'patch', 'delete')       

    singular_commands = ('retrieve', 'update', 'destroy')
    data_commands = ('create', 'update')


    def create_attr(self, resource, command, *args, **kwargs):
        url = f'{self.base_api_url}{resource}/'
        args_offset = 0
        # TODO: maybe add validation for parameter depending on command like create needs only one
        data = None
        if command in self.singular_commands: # TODO: this is super dangerous, maybe user kwargs...
            pk = args[args_offset]
            args_offset += 1
            url += str(pk)
        if command in self.data_commands:
            data = args[args_offset]
            args_offset += 1
        print(url)
        # TODO: reaplace None with proper stuff
        request_kwargs = {
            'params': None,
            'data': data,
            'headers': None,
            'auth': None,
            'cookies': None
        }
        r = requests.request(self.commands_to_methods[command], url, **request_kwargs)
        return r

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
            'commands': ('create', 'retrieve', 'update', 'destroy', 'list'),
            'data': {
                'name': {'required': True}
            }
            # 'subresources': ('posboxes') or define it anew, but not going to implement this for now
        },
        'postboxes': {
            'commands': ('retrieve',)
        }
    }


conn = ImplementedAPIConnector()
print(conn.users_list())
