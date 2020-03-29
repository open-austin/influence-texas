#!/usr/bin/env bash
DIR=`dirname $BASH_SOURCE`
# this will build the frontend assets inside a docker contianer 
docker rm itreactrun || true 
docker build -t itreact $DIR/../frontend
# `npm install` and `npm run build` both take a minute
docker run --ipc=host --name=itreactrun itreact 
# copy the newly built files to the host
docker cp itreactrun:/usr/src/influencetx/static/react-app $DIR/../influencetx/static
# and open so you can see it worked
open  $DIR/../influencetx/static/react-app/index.html
