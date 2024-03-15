As described in `ARCHITECTURE.md`, the system mainly has 3 components:
1) The API Server
2) The Huey Worker
3) The Redis DB

In this doc, we'll see how to make changes to the source code of the first two components, build your Docker images, push them to Docker Hub, and finally run the containers in your K8s Cluster.

## API Server
The `server` directory contains the code of the API server component, that is powered by FAST API.

In order to build a Docker image of the API Server, we can use the `docker_build_server.sh` script available in the same directory.

But, let's take a look at a couple of things in the script first.

```
#!/bin/bash

ln -fs .dockerignore.server .dockerignore

docker build -f Dockerfile.server -t abhilakshsinghreen/key-value-store-api-server .
```

The first statement, links `.dockerignore.server` to `.dockerignore`. This is required as `docker build` does not have support for passing in a custom dockerignore file. In `ARCHITECTURE.MD`, we discuss why the server and worker code is not put into separate directories.

The second statement, build the Docker image using `Dockerfile.server` as the input DockerFile. By default, the image is tagged `abhilakshsinghreen/key-value-store-api-server`. In order to upload this image to your own Docker Registry, please change the tag accordingly.


## Huey Worker
Quite similar to the API Server, the Huey Worker Docker image can be built using `docker_build_worker.sh`. It also links `.dockerignore.worker` to `.dockerignore` and tags the image.

## Deploying YOUR containers on K8s
Once you've built and pushed the API Server and Huey worker images to your Docker Registry, we can deploy them in a K8s Cluster.

Let's assume, we have the images `exampleperson/key-value-store-api-server` and `exampleperson/key-value-store-api-server`.

We need to make two updates to use the custom images.
First, in `kubernetes/worker/server.yaml` at line 19, we will specify the API Server image.

And second, open up `kubernetes/worker/worker.yaml` and move to line 19. Here, we will specify the custom worker image.

With these changes made, we can follow the steps in `DEPLOYMENT.md` to deploy on K8s.
