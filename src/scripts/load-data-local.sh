#!/usr/bin/env bash

# arg: MAX_BILLS - set maximum number of bills to sync.
# The number of bills in the database is quite large. For testing purposes, you can grab a subset of the data
# ex: MAX_BILLS=100 bash load-data-local.sh

docker exec -it inftxos_web_1 python manage.py sync_legislators_from_openstate
docker exec -it inftxos_web_1 python manage.py sync_bills_from_openstate --max ${MAX_BILLS:-100}
