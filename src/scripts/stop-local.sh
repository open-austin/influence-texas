#!/usr/bin/env bash
# Automatically shut down all influence texas containers
echo "Shutting down inftxos containers"
docker ps -q -f name="inftxos*" | while read CONTAINER ; do docker stop $CONTAINER ; done
echo "Done"
