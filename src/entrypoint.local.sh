#!/usr/bin/env bash
set -o errexit

# Start outputting logs to stdout
tail -n 0 -f ../logs/gunicorn*.log &

# Loop sleep every second until a db connection is available.
until psql $DATABASE_URL -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping ..."
  sleep 1
done
>&2 echo "Postgres is up - executing command"

# Run migrations
python3 manage.py migrate

echo "Migrations done. Running at http://localhost:5120"

exec "$@"
