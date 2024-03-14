#!/bin/bash

ln -fs .dockerignore.worker .dockerignore

docker build -f Dockerfile.worker -t cache-api-worker .
