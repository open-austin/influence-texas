#!/usr/bin/env bash
echo "sh: docker exec -it inftxos_web_1 python manage.py $@"
docker exec -it inftxos_web_1 python manage.py $@
