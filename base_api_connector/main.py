import requests
import inspect


POSSIBLE_COMMANDS = ('list', 'create', 'retrieve', 'update', 'destroy')


class CommandMethodHolder:  # TODO: upgrade Response object r with helpful stuff like accessing the id when using create
    def get_full_url(self, pk=None):
        raise NotImplementedError

    def list(self):  # TODO: also, do I want validation for data?
        def list(**kwargs):
            url = self.get_full_url()
            r = requests.get(url, **kwargs)
            return r
        return list

    def create(self):
        def create(data, **kwargs):
            if isinstance(data, AsDictObject):
                data = data.as_dict()
            url = self.get_full_url()
            r = requests.post(url, data, **kwargs)
            return r
        return create

    def retrieve(self):
        def retrieve(pk, **kwargs):
            url = self.get_full_url(pk)
            r = requests.get(url, **kwargs)
            return r
        return retrieve

    def update(self):
        def update(pk, data, **kwargs):
            if isinstance(data, AsDictObject):
                data = data.as_dict()
            url = self.get_full_url(pk)
            r = requests.patch(url, data, **kwargs)
            return r
        return update

    def delete(self):
        def delete(pk, **kwargs):
            url = self.get_full_url(pk)
            r = requests.delete(url, **kwargs)
            return r
        return delete


class APIResource:
    def __init__(self, Connector, resource, settings=None, *args, **kwargs):
        self.name = resource
        self.API = Connector

        for setting, content in settings.items():
            if setting == 'commands':
                if content == 'all':
                    content = POSSIBLE_COMMANDS
                for command in content:
                    if hasattr(CommandMethodHolder, command):
                        setattr(self, command, getattr(CommandMethodHolder, command)(self))

        # return super().__init__(*args, **kwargs) # TODO: do I need this look it up

    def get_full_url(self, pk=''):
        return f'{self.API.base_api_url}{self.name}/{pk}'

    def get_headers(self):
        pass  # TODO: implement defaults for headers and anything else you can think of


class GenericAPIConnector:
    def __new__(cls):
        for resource, settings in cls.resource_config.items():
            setattr(cls, resource, APIResource(cls, resource, settings))

        return object.__new__(cls)
# TODO: maybe add init where you can put the config and stuff in without having to create a new class
    base_data = {}
    base_header = {}

    @property
    def base_api_url(self):
        raise NotImplementedError()

    @property
    def resource_config(self):
        raise NotImplementedError()


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

                if callable(value):
                    dict_repr[name] = value()
                else:
                    dict_repr[name] = value
        return dict_repr
