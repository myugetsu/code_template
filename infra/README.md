To run the project locally you can simply install `minikube (https://minikube.sigs.k8s.io/docs/start/)` or if you are on a `k8s (https://kubernetes.io/docs/tasks/tools/)` server simply follow the instructions below

To deploy the database
``` sh
  $ kubectl apply -f mysql-deployment.yaml
```

To deploy the application
``` sh
  $ kubectl apply -f deployment.yaml
  $ kubectl apply -f service.yaml
```

To access your Flask app
``` sh
  $ kubectl get svc flask-app-service
```
Get the IP and port of the LoadBalancer service using: (when using minikube)
``` sh
  $ minikube service flask-app-service --url
```
o access your Flask app, you need to find the IP and port of the Pod running your app.
You can use a service or port-forwarding to access it. To port-forward to the pod:
```sh
  kubectl port-forward pod/flask-app-deployment-<pod-id> 5000:5000
```
