from .main import GenericAPIConnector, AsDictObject


class UserObject(AsDictObject):
    name = 'test'


class ImplementedAPIConnector(GenericAPIConnector):
    base_api_url = 'http://127.0.0.1:8000/notes-backend/'
    resource_config = {
        'users': {
            'commands': ('create', 'retrieve', 'update', 'destroy', 'list'),
            'params': {  # TODO: I do want to define params here
                'filter_option': {}  # maybe in a list
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
        },
        'types': {
            'commands': ('create', 'retrieve', 'update', 'destroy', 'list'),
        }
    }


# conn = ImplementedAPIConnector()
# print(conn.notes.list())
# print(dir(CommandMethodHolder))
