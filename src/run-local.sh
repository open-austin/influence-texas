#!/usr/bin/env bash
set -o errexit
DIR=`dirname $BASH_SOURCE`

# Build a docker image using your local configs
DOCKER_BUILDKIT=1 docker build --build-arg APP_ENV=nick -f $DIR/Dockerfile.nick -t inftxos:local $DIR

# Source your env variables for use in docker-compose
source $DIR/env.sh
export COMPOSE_PROJECT_NAME=inftxos

# Run it
docker-compose -f $DIR/docker-compose.nick up
