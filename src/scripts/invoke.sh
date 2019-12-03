#!/usr/bin/env bash
echo "sh: docker exec -it inftxos_web_1 invoke $@"
docker exec -it inftxos_web_1 invoke $@
