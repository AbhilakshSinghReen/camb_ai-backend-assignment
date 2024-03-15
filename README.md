# Deploy on Kubernetes
## Prerequisites
In order to procees with deployment on your Kubernetes cluster, you need to have a K8s Cluster up an running. For the purpose of this guide, I will be using `minikube`.
Apart from this, you should also have `kubectl` and `helm` installed.

## Get the Code
Clone this repository
`git clone https://github.com/AbhilakshSinghReen/camb_ai-backend-assignment.git`

Move into the project folder
`cd camb_ai-backend-assignment`

## Deployment
### Setup K8s namespace
To manage the resouces of our project, we'll be creating a K8s namespace called `key-value-store`
`kubectl create namespace key-value-store`

### Setup Redis
For running Redis, in our cluster, we'll be using the Helm chart provided by Bitname.

Add the Bitnami repo to Helm.
`helm repo add bitnami https://charts.bitnami.com/bitnami`

Install the help chart. The installation uses values defined in `kubernetes/redis/redis-values.yaml`
`helm install key-value-store-redis bitnami/redis --values kubernetes/redis/redis-values.yaml -n key-value-store --set auth.enabled=false`

Create the ConfigMap for Redis.
`kubectl apply -f kubernetes/redis/redis-configmap.yaml -n key-value-store`

### Setup Huey Worker
In order to setup the Huey worker, we have to create three resources. The `kubernetes/worker/worker.yaml` file defines the deployment and the corresponding ClusterIP service. In addition, we can also provision Horizontal Pod Autoscaling using the HorizontalPodAutoscaler defined in `kubernetes/worker/worker-hpa.yaml`.

Create the deployment and service for the Huey Worker.
`kubectl apply -n key-value-store -f kubernetes/worker/worker.yaml`

Create the HorizontalPodAutoscaler (Optional)
`kubectl apply -n key-value-store -f kubernetes/worker/worker-hpa.yaml`

### Setup Server
Similar to the Huey Worker, we will need three (one optional) resources for the Server.

Deployment and ClusterIP Service
`kubectl apply -n key-value-store -f kubernetes/server/server.yaml`

HorizontalPodAutoscaler (Optional)
`kubectl apply -n key-value-store -f kubernetes/server/server-hpa.yaml`

In addition, if we want the server to be accessed from outside the Cluster, we have to create an Ingress or a LoadBalancer service. For the purpose of this demo, we'll be using a LoadBalancer Service. This can be created by running the following:
`kubectl apply -n key-value-store -f kubernetes/server/server-loadbalancer-service.yaml`
