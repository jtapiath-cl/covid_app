#!/bin/bash

git pull

docker stop covid_app

python3 setup.py

docker build \
    -t covid_app:latest \
    .

docker run \
    --detach \
    --publish 8050:8050 \
    --rm \
    --hostname prd_env \
    --name covid_app \
    --volume $(pwd):/app \
    covid_app:latest
