# zoomapi

[https://github.com/crista/zoomapi](https://github.com/crista/zoomapi)

Python wrapper around the [Zoom.us](http://zoom.us) REST API v2.

This work is based on [Zoomus](https://github.com/actmd/zoomus), but with OAuth support.

## Compatibility

Note, as this library heavily depends on the [requests](https://pypi.org/project/requests/) library, official compatibility is limited to the official compatibility of `requests`.

## Example Usage

### Create the client 

```python
import json
from zoomapi import OAuthZoomClient

client = OAuthZoomClient('CLIENT_ID', 'CLIENT_SECRET', 'REDIRECT_URL')

user_response = client.user.get(id='me')
user = json.loads(user_response.content)
print(user)
```

What one will note is that the returned object from a call using the client is a [requests](https://pypi.org/project/requests/) `Response` object. This is done so that if there is any error working with the API that one has complete control of handling all errors. As such, to actually get the list of users in the example above, one will have to load the JSON from the content of the `Response` object that is returned.

### Using with a manage context

```python
with JWTZoomClient('API_KEY', 'API_SECRET') as client:
    user_list_response = client.users.list()
    ...
```

## Available methods

* client.user.create(...)
* client.user.cust_create(...)
* client.user.update(...)*
* client.user.list(...)
* client.user.pending(...)
* client.user.get(...)
* client.user.get_by_email(...)

* client.meeting.get(...)
* client.meeting.end(...)
* client.meeting.create(...)
* client.meeting.delete(...)
* client.meeting.list(...)
* client.meeting.update(...)

* client.report.get_account_report(...)
* client.report.get_user_report(...)

* client.webinar.create(...)
* client.webinar.update(...)
* client.webinar.delete(...)
* client.webinar.list(...)
* client.webinar.get(...)
* client.webinar.end(...)
* client.webinar.register(...)

