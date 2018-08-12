#!/bin/bash -x

# Prepare log files and start outputting logs to stdout
touch logs/gunicorn.log
touch logs/gunicorn-access.log
tail -n 0 -f logs/gunicorn*.log &

export DJANGO_SETTINGS_MODULE=config.settings.production
exec gunicorn config.wsgi \
    --name influencetx \
    --bind 0.0.0.0:5120 \
    --workers 3 \
    --log-level=info \
    --log-file=./logs/gunicorn.log \
    --access-logfile=./logs/gunicorn-access.log \
