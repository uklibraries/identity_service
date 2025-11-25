#!/bin/bash
set -e

uv run manage.py collectstatic --noinput
uv run manage.py migrate --noinput
# db reset
uv run manage.py syncdata /initial-data/initial-data.json
# load prod data
# ...
uv run gunicorn identity.wsgi --bind 0.0.0.0:8000 --workers 3
