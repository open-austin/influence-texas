#!/usr/bin/env bash
echo "sh: docker exec -it web python manage.py $@"
docker exec -it web python manage.py $@
