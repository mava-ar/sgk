#!/bin/sh
echo "{ \"allow_root\": true }" > ~/.bowerrc
python manage.py migrate
python manage.py bower_install
python manage.py collectstatic --noinput
python manage.py runserver_plus 0.0.0.0:8000
