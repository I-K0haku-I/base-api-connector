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
                    if content == 'all':
                        content = cls.possible_commands
                    for command in content:  # TODO: maybe make multiple lambdas depending on command or some magic stuff
                        setattr(cls, f'{resource}_{command}', lambda self, *a, resource=resource,
                                command=command, **kw: self.create_attr(resource, command, *a, **kw))
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
        # TODO: this is super dangerous, maybe use kwargs...
        if command in self.singular_commands:
            pk = args[args_offset]
            args_offset += 1
            url += str(pk)
        if command in self.data_commands:
            data = args[args_offset]
            args_offset += 1
        print(self.commands_to_methods[command], url)
        # TODO: reaplace None with proper stuff
        request_kwargs = {
            'params': None,
            'data': data,
            'headers': None,
            'auth': None,
            'cookies': None
        }
        r = requests.request(self.commands_to_methods[command], url, **request_kwargs)
        # TODO: decide what to return, preferably only what you would actually use, idk how though
        if r.ok:
            return r.json()
        return r

    base_data = {}
    base_header = {}

    @property
    def base_api_url(self):
        raise NotImplementedError()

    @property
    def resource_config(self):
        raise NotImplementedError()


class UserObject(AsDictObject):
    name = 'test'


class ImplementedAPIConnector(GenericAPIConnector):
    base_api_url = 'http://127.0.0.1:8000/notes-backend/'
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
        },
        'notes': {
            'commands': 'all',
        },
        'tags': {
            'commands': ('create', 'retrieve', 'update', 'destroy', 'list'),
            'data': {
                'name': {'required': True}
            }
        },
        'types': {
            'commands': ('create', 'retrieve', 'update', 'destroy', 'list'),
        }
    }


conn = ImplementedAPIConnector()
print(conn.notes_create({}))
