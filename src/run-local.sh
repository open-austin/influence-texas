#!/usr/bin/env bash
set -o errexit
DIR=`dirname $BASH_SOURCE`

# Build a docker image using your local configs
docker build --build-arg APP_ENV=nick -f $DIR/Dockerfile.nick -t inftxos:local $DIR

# Source your env variables for use in docker-compose
source $DIR/env.sh

# Run it
docker-compose -f $DIR/docker-compose.nick up

# exec "$@" isn't working
# ideally
# docker run -it inftxos:local bin/bash
# would be sufficient
# docker run -it --entrypoint /bin/bash inftxos:local
