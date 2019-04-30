# Base API Connector

Helps create a simple API Connector where all you have to do is define the resources and possible commands in a config.


## Example

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
            'commands': ('create', 'retrieve', 'update'),
            'data': {
                'content': {},
                'author': {'required': True},
            }
        }
        'users': {
            'commands': 'all',
            'data': {
                'name': {'required': True}
            }
        },
        ...
    }
```
This will generate the following attributes when you use this class:

```
conn = ImplementedAPIConnector()

conn.reports.create(data)
conn.reports.retrieve(id)
conn.reports update(id, data)

conn.users.list()
conn.users.create(data)
conn.users.retrieve(id)
conn.users.update(id, data)
conn.users.delete(id)
```

Those methods return a regular Response object from the requests module.