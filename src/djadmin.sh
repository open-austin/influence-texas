#!/usr/bin/env bash
echo "sh: docker-compose exec web python manage.py $@"
docker-compose exec web python manage.py $@

