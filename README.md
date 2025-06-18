identity_service
================

`identity_service` is an [ARK and NOID](https://arks.org)-based Identity service
written in [Django](https://www.djangoproject.com/) and the
[Django REST framework](https://www.django-rest-framework.org/)
with [DRF-SimpleJWT](https://github.com/jazzband/djangorestframework-simplejwt).

This software is still in development flux.


Installation
------------

For development, you will need [Docker](https://www.docker.com/).

Install and extract the code:

```
git clone git@github.com:uklibraries/identity_service.git
```

Start things up:

```
docker compose up
```

This will start a Django server on port 8000 by default.

Run tests:

```
docker exec -it ukl-identity-dj bash
$ uv run pytest-watcher .
```

Note: this is currently watching all tests, both unit and integration.


License
-------

Copyright (C) 2024-2025 MLE Slone. Licensed under the [MIT license](LICENSE.md).
