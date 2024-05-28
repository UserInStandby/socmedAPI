#!/bin/sh
if [ "$SERVICE_NAME" = "socmedapi" ]
then
python manage.py wait_for_db
python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate
fi

