#!/bin/bash

docker build \
    -t covid_app:latest \
    .

wait(5)

docker run \
    --detach \
    --publish 8050:8050 \
    --rm \
    --hostname prd_env \
    --name covid_app \
    covid_app