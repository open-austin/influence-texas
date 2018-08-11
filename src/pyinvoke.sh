#!/usr/bin/env bash
echo "sh: docker-compose exec web invoke $@"
docker-compose exec web invoke $@

