#!/bin/bash

# Prepare log files and start outputting logs to stdout
mkdir ./logs
touch ./logs/gunicorn.log
touch ./logs/gunicorn-access.log
tail -n 0 -f ./logs/gunicorn*.log &

exec gunicorn config.wsgi:application \
    --name influencetx \
    --bind 0.0.0.0:5120 \
    --workers 5 \
    --log-level=info \
    --log-file=./logs/gunicorn.log \
    --access-logfile=./logs/gunicorn-access.log \
"$@"
