#!/bin/bash

NAME="kines"                                  # Name of the application
USER_HOME=/home/matuu
DJANGODIR=${USER_HOME}/kines/sgk/src  # Django project directory
SOCKFILE=${USER_HOME}/kines/run/gunicorn.sock  # we will communicte using this unix socket
USER=matuu                                       # the user to run as
GROUP=matuu                                     # the group to run as
NUM_WORKERS=3                                     # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=sgk.settings.production             # which settings file should Django use
DJANGO_WSGI_MODULE=sgk.wsgi                     # WSGI module name

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR
source ${USER_HOME}/kines/venv/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec ${USER_HOME}/kines/venv/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --bind=unix:$SOCKFILE \
  --log-level=debug \
  --log-file=-
