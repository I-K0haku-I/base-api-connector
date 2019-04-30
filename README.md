# Base API Connector

Helps create a simple API Connector where all you have to do is define the resources and possible commands in a config.

## Instructions

### Using GenericAPIConnector

First import the GenericAPIConnector class:

```
from base_api_connector import GenericAPIConnector
```

Then, define a base_api_url and a resource_config like this:

```
class ImplementedAPIConnector(GenericAPIConnector):
    base_api_url = 'http://127.0.0.1:8000/api/'
    resource_config = {
        'reports': {
            'commands': ('create', 'retrieve', 'update')
        }
        'users': {
            'commands': 'all'
        },
        ...
    }
```
This will generate the following attributes when you use this class:

```
conn = ImplementedAPIConnector()

conn.reports.create(data)
conn.reports.retrieve(pk)
conn.reports update(pk, data)

conn.users.list()
conn.users.create(data)
conn.users.retrieve(pk)
conn.users.update(pk, data)
conn.users.delete(pk)
```

They accept dict for data like the normal requests module and AsDictObject found in this package.

### Using The Returned Object

The methods of GenericAPIConnector return a regular Response object from the requests module. See requests [Documentation for Response](https://2.python-requests.org/en/latest/api/#requests.Response) for more details.


### Using AsDictObject (WIP)

If you want to define how a resource looks only once, import AsDictObject:
```
import datetime
from base_api_connecotr import AsDictObject

class CreateUsersResourceObject(AsDictObject):
    name = None  # None will not pass the field in the request
    created = datetime.datetime.now  # use methods to set defaults like this
    created_for_app = 'readme_example'
```

And then use it like this:
```
user = CreateUsersResourceObject():
user.name = 'readme user'
conn.users.create(user)
```