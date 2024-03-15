In this document, we will first take a look at the System's architecture in a Cluster and discuss high-level design decisions. In the second part, we discuss the low-level design and how the codebase is structured.

## High-Level Design

## Low-Level Design
The folder structure is as follow:
1) `server` contains the source code of the API Server and Huey Worker.
2) `kubernetes` contains K8s manifests required for deployment.
3) `tests` contains Unit Tests, API Tests, and Load Tests.

### server (and worker)
The API Server and Huey Worker are built into two different Docker images. But, since both of the applications have multiple files in common, they are structured in the same folder.

##### Alternative approaches and trade-offs
1) An alternate approach would be to use three folders such as `server`, `worker`, and `common`, in which the first two contain the server and worker files and the last one contains the common files required by both. -- This approach has two problems:
a) It complicates the process of building Docker images.
b) Most IDEs will not provide IntelliSense on the files contained in the `common` folder when one is working in the other two folders.

2) Another alternative approach could be to duplicate the files from the `server` folder to `worker`. -- This approach also has some issues:
a) The files may by unsynchronized.
b) The codebase now contains redundant files.

#### Dockerfiles and dockerignores
Both the API Server and Huey Worker have their own requirements file, Dockerfile, dockerignore, and docker_build script.
For more information on how to build the Docker images, check out `DOCKER_BUILD.md`.

The `src` folder contains the primary package code. Here's a quick overview of all the files in it:
1) `app.py`: the FAST API application.
2) `models.py`: Pydantic Models required for the FAST API application (Request Schemas).
3) `redis_client.py`: contains a Redis Client that connect to a Redis Server based on the configuration specified in environment variables.
4) `tasks.py`: contains the Huey instance and Huey tasks
5) `templating.py`: contains utils for dealing with HTML templates.

The API Server requires all the files in the `src` folder, whereas the Huey Worker only requires the `redis_client.py` and `tasks.py`.

The `main.py` file is only for running the API Server in development.

The `templates` directory contains HTML templates corresponding to certain routes.

#### Open API
If you have the API Server deployed or running in development, it is possible to access the Open API specification or the Swagger Page by visiting `{{serverUrl}}/openapi.json` or `{{serverUrl}}/docs` respectively.

### kubernetes
The `kubernetes` folder contains three sub-folders, corresponding to the components described in the High-Level Design section.

For more information on deploying the system on a K8s Cluster, check out `DEPLOYMENT.md`.

### tests
This directory contains 3 main types of tests:
1) Unit Tests (Right now, only for the server): Test the Fast API Application using the FAST API Test Client - `test_server_app.py`
2) API Tests: For testing the APIs after deployment - `apis_test.py`
3) API Load Tests: For load testing the APIs after deployment - `apis_load_test.py`

For Unit Testing, we use `Pytest`. Running `pytest` on the tests dir will only run the tests container in `test_server_app.py`.
