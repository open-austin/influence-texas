#!/usr/bin/env bash
set -o errexit

# Start outputting logs to stdout
tail -n 0 -f ../logs/gunicorn*.log &

# Only use raven for production environments?
# export DJANGO_SETTINGS_MODULE=config.settings.production

# Run migrations
python3 manage.py migrate

echo "Done"

exec "$@"
