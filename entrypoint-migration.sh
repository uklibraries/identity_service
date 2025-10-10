#!/bin/bash
set -e

uv run manage.py makemigrations
uv run manage.py migrate
uv run manage.py createcachetable
uv run manage.py syncdata /initial-data/initial-data.json
