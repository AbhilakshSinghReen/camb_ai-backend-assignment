# Deploy on Kubernetes
## Prerequisites
In order to procees with deployment on your Kubernetes cluster, you need to have a K8s Cluster up an running. For the purpose of this guide, I will be using `minikube`.
Apart from this, you should also have `kubectl` and `helm` installed.

## Get the Code
Clone this repository <br>
```
git clone https://github.com/AbhilakshSinghReen/camb_ai-backend-assignment.git
```

Move into the project folder
```
cd camb_ai-backend-assignment
```

## Deployment
### Setup K8s namespace
To manage the resouces of our project, we'll be creating a K8s namespace called `key-value-store`
```
kubectl create namespace key-value-store
```

### Setup Redis
For running Redis, in our cluster, we'll be using the Helm chart provided by Bitnami.

Add the Bitnami repo to Helm.
```
helm repo add bitnami https://charts.bitnami.com/bitnami
```

Install the help chart. The installation uses values defined in `kubernetes/redis/redis-values.yaml`
```
helm install key-value-store-redis bitnami/redis --values kubernetes/redis/redis-values.yaml -n key-value-store --set auth.enabled=false
```

Create the ConfigMap for Redis.
```
kubectl apply -f kubernetes/redis/redis-configmap.yaml -n key-value-store
```

### Setup Huey Worker
In order to setup the Huey worker, we have to create three resources. The `kubernetes/worker/worker.yaml` file defines the deployment and the corresponding ClusterIP service. In addition, we can also provision Horizontal Pod Autoscaling using the HorizontalPodAutoscaler defined in `kubernetes/worker/worker-hpa.yaml`.

Create the deployment and service for the Huey Worker.
```
kubectl apply -n key-value-store -f kubernetes/worker/worker.yaml
```

Create the HorizontalPodAutoscaler (Optional)
```
kubectl apply -n key-value-store -f kubernetes/worker/worker-hpa.yaml
```

### Setup Server
Similar to the Huey Worker, we will need three (one optional) resources for the Server.

Deployment and ClusterIP Service
```
kubectl apply -n key-value-store -f kubernetes/server/server.yaml
```

HorizontalPodAutoscaler (Optional)
```
kubectl apply -n key-value-store -f kubernetes/server/server-hpa.yaml
```

In addition, if we want the server to be accessed from outside the Cluster, we have to create an Ingress or a LoadBalancer service. For the purpose of this demo, we'll be using a LoadBalancer Service. This can be created by running the following:
```
kubectl apply -n key-value-store -f kubernetes/server/server-loadbalancer-service.yaml
```

### Verify Resources Creation
Let's first get the running pods.
```
kubectl get pods -n key-value-store
```

The ouput should show the following three pods:
1) At least one pod prefixed with `key-value-store-api-server`
2) At least one pod prefixed with `key-value-store-api-worker`
3) At least one pod prefixed with `key-value-store-redis-master`

Now, let's verify the services
```
kubectl get services -n key-value-store
```

The output should show at least the following four services:
1) `key-value-store-redis-master`
2) `key-value-store-api-worker-service`
3) `key-value-store-api-server-service`
4) `key-value-store-api-server-loadbalancer-service`

Finally, let's verify the available HPA resources.
```
kubectl get hpa -n key-value-store
```

The output should show at least the following two HPAs:
1) `key-value-store-api-server`
2) `key-value-store-api-worker`

### Running Tests
For running tests, it is required to have the server accessible from outside the Cluster. When using `minikube`, we will need to start a tunnel for our LoadBalancer service.
```
minikube tunnel
```
The output should show `Starting tunnel for service key-value-store-api-server-loadbalancer-service.`

You can try visiting `http://locahost:8000` in your browser and see a page titled "CAMB.AI - Backend Assignment".

Inside your local development environment, cd into the `tests` folder and install the required packages. It is recommended to use a virtual environment.
```
pip install -r requirements.txt
```

Next, run the API tests using:
```
python3 api_tests.py
```

You should get an output saying that 7 tests have passed.

To tests the APIs using the Swagger page, you can visit `http://locahost:8000/docs` in your browser.

### Testing HPA by Load Testing
For this purpose, the LoadBalancer service should be accessible from outside the cluster.

Start tracking the HPA resource by running:
```
kubectl get hpa -n key-value-store key-value-store-api-server --watch
```

We will need a new terminal to load the server. Inside a new terminal, run the following command:
```
while sleep 0.01; do wget -q -O- http://localhost:8000/docs; done
```
This attempts to make a `GET` request to the docs page every 10 ms.

Head back to the terminal watching the HPA resource.
You should see the number of replicas increasing.

If we list the available pods using
```
kubectl get pods -n key-value-store
```

We should see that one or more replicas of the `key-value-store-api-server` pod have been created.
