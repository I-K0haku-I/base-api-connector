# Base API Connector

Helps create a simple API Connector where all you have to do is define the resources and possible commands.

## Instructions

### Using the Module

First import the GenericAPIConnector class:

```
from base_api_connector import GenericAPIConnector
```

Then, define a base_api_url and resource fields like this:

```
class ImplementedAPIConnector(GenericAPIConnector):
    base_api_url = 'http://127.0.0.1:8000/notes-backend/'
    reports = APIResource(('create', 'retrieve', 'update'))
    users = APIResource('all')
```
That will generate the following attributes when you use the class:

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

### Asyncio

You can tell tell your resource fields that they should be accessed with asyncio per default:
```
class ImplementedAPIConnector(GenericAPIConnector):
    # ...
    users = APIResource('all', is_async=True)
```
and then use it in an async metho as follows:
```
async def create_user(user):
    r = await conn.user.create(user)
    data = await r.json()
    # ...
```
Alternatively, you can change switch to async in-line as well:
```
    # ...
    r = await conn.reports(is_async=True).list()
    # ...
```
or the other way around:
```
r = conn.user(is_async=False).list()
```

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