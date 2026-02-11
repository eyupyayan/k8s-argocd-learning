# Kubernetes + Argo CD + Monitoring Demo

Dette prosjektet er et læringsprosjekt for å forstå:

- Docker container bygging og publishing
- Kubernetes manifests
- Kustomize base + overlays (dev / prod)
- Argo CD GitOps
- Horizontal Pod Autoscaler (HPA)
- Prometheus + Grafana monitoring

## Struktur

```

app/            -> Python FastAPI app
k8s/
myapp/
base/       -> Felles manifests
overlays/
dev/      -> Dev patches
prod/     -> Prod patches
apps/         -> Argo CD Applications
monitoring/   -> Prometheus + Grafana

````

---

## 1. Bygge og pushe app

```bash
cd app
docker build -t <dockerhub_user>/myapp:0.2.0 .
docker push <dockerhub_user>/myapp:0.2.0
````

---

## 2. Kubernetes (lokal test)

Aktiver Kubernetes i Docker Desktop.

Installer metrics-server (for HPA):

```bash
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

Deploy dev:

```bash
kubectl apply -k k8s/myapp/overlays/dev
```

---

## 3. Argo CD

Installer Argo CD:

```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/master/manifests/install.yaml
```

Port-forward UI:

```bash
kubectl -n argocd port-forward svc/argocd-server 8080:443
```

---

## 4. Monitoring (Prometheus + Grafana)

Monitoring installeres via Argo CD Helm chart
Namespace `monitoring` opprettes automatisk av Argo CD.

Grafana tilgang:

```bash
kubectl -n monitoring port-forward svc/monitoring-grafana 3000:80
```

---

## 5. HPA test

Generer last:

```bash
while true; do curl http://localhost:8081/work?ms=500; done
```

Se autoskalering:

```bash
kubectl get hpa -w
```

---

## Miljøer

| Miljø | Namespace  | Replicas | HPA  |
| ----- | ---------- | -------- | ---- |
| Dev   | myapp-dev  | 1        | 1-5  |
| Prod  | myapp-prod | 3        | 3-10 |

---

## Læringsmål

* Forstå GitOps workflow
* Skille mellom base og overlays
* Observere autoskalering
* Visualisere metrics i Grafana

```

---

Dette README-oppsettet gjør at:
- du dokumenterer *hele reisen*
- du kan vise prosjektet som portfolio
- du slipper å glemme hvorfor noe ble gjort senere 😄
```
