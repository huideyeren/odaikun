#! /usr/bin/env bash

docker-compose run backend pytest -v
docker-compose run frontend test