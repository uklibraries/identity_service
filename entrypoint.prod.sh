#!/bin/bash
set -e

uv run manage.py collectstatic --noinput
uv run manage.py migrate --noinput
# note: data should be loaded via Postgres, not Django

uv run gunicorn identity.wsgi --bind 0.0.0.0:8000 --workers 3
