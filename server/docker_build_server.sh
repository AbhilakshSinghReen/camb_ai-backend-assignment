#!/bin/bash

ln -fs .dockerignore.server .dockerignore

docker build -f Dockerfile.server -t cache-api-server .
