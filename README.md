identity_service
================

`identity_service` is an [ARK and NOID](https://arks.org)-based Identity service
written in [Django](https://www.djangoproject.com/) and the
[Django REST framework](https://www.django-rest-framework.org/).

This software is still in development flux.


Installation
------------

For development, you will need:

* [Python](https://www.python.org/) - currently tested with 3.13
* [Poetry](https://python-poetry.org/)
* [SQLite](https://www.sqlite.org/)

Install and extract the code:

```
git clone git@github.com:uklibraries/identity_service.git
```

Run a server (useful for poking around, not needed for testing):

```
cd identity_service
poetry install --no-root
poetry run python manage.py migrate
poetry run python manage.py runserver
```

Run tests:

```
poetry run pytest-watcher .
```

Note: this is currently watching all tests, both unit and integration.


License
-------

Copyright (C) 2024 MLE Slone. Licensed under the [MIT license](LICENSE.md).

This project incorporates the [UpdateMixin](https://github.com/encode/django-rest-framework/discussions/8606#discussioncomment-3899252)
by [Kangaroux](https://github.com/Kangaroux).

This project incorporates the [ValidateFieldsMixin](https://github.com/encode/django-rest-framework/issues/1655#issuecomment-1110743102)
by [dmugtasimov](https://github.com/dmugtasimov).
