#!/usr/bin/env bash

set -e

RUN_MANAGE_PY='poetry run python3 -m washday.manage'

echo 'Collecting static files...'
$RUN_MANAGE_PY collectstatic --no-input

echo 'Running migrations...'
$RUN_MANAGE_PY migrate --no-input

exec poetry run python3 -m washday.manage runserver 0.0.0.0:8000
