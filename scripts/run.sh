#!/bin/sh

python manage.py wait_for_db
python manage.py collectstatic --noinput
