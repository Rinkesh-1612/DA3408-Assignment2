# DA3408 — Module 3 Assignment: Infrastructure & Containerization

A spam/ham text classifier (TF-IDF + Naive Bayes) packaged and deployed four different
ways across Docker and Kubernetes, per the Module 3 assignment brief (`Assignment 2.pdf`).

## What's in here

```
.
├── train.py                  # generates the dataset + trains the model
├── requirements.txt
├── app/main.py                # FastAPI service: POST /predict, GET /healthz
├── Dockerfile.naive           # Q1: single-stage build
├── Dockerfile                 # Q1: multi-stage build (also used by Q2 and Q4)
├── docker-compose.yml         # Q2: api + Redis cache
├── q3-data-validation/        # Q3: standalone Kubernetes Indexed Job
│   ├── generate_shards.py
│   ├── validation.py
│   ├── job.yaml
│   └── shards/
├── q4-deployment/             # Q4: Kubernetes Deployment + Service
│   ├── deployment.yaml
│   └── service.yaml
├── reportDA3408A2.pdf                 # written answers for all four questions
├── evidence/                  # screenshots and logs referenced in the report
└── AI_DISCLOSURE.md
```

## The app

`train.py` generates a deterministic 1000-row synthetic dataset (seeded), trains a
`TfidfVectorizer` + `MultinomialNB` pipeline, and saves it with `joblib`. `app/main.py`
loads that model at startup and exposes:

- `POST /predict` — `{"text": "..."}` → `{"label": "spam"}` or `{"label": "ham"}`
- `GET /healthz` — `200` once the model is loaded, `503` otherwise

## Q1 — Docker: naive vs. multi-stage

```bash
docker build -f Dockerfile.naive -t spam-api:naive .
docker build -t spam-api:multistage .
docker images spam-api
```

Both stages use the same `python:3.12` base image (no `-slim`), so the size difference
comes purely from what the multi-stage build excludes from its final image — not from a
smaller base. Naive image: 1513.3 MiB. Multi-stage image: 1426.7 MiB (5.72% smaller).
Both run and serve `/predict` + `/healthz` identically — see `evidence/q1-image-sizes/`
and `reportDA3408A2.pdf` for the full comparison and reasoning.

## Q2 — Docker Compose with Redis caching

```bash
docker compose up --build
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "WIN a FREE iPhone now!"}'
```

Send the same request twice — the second call is served from Redis (cache hit) instead
of re-running the model. Both requests log a `CACHE MISS`/`CACHE HIT` line with timing
(29.45ms vs 0.35ms — see `evidence/q2-compose-cache/`).

## Q3 — Kubernetes Indexed Job

A separate batch workload: 8 CSV shards of signup records, each validated by one pod in
an Indexed Job.

```bash
cd q3-data-validation
python3 generate_shards.py                    # writes shards/shard-0.csv .. shard-7.csv
docker build -t shard-validator:v1 .
minikube image load shard-validator:v1
kubectl apply -f job.yaml
kubectl get pods -o wide                      # watch parallelism (4) in action
kubectl logs -l job-name=shard-validator-job --prefix=true
```

Each pod reports its shard's invalid-row count via its own logs, read through the
Kubernetes API — no shared volume involved. See `evidence/q3-indexed-job/` for the full
run, including node distribution and the matching ground-truth counts.

## Q4 — Kubernetes Deployment: self-healing and rolling updates

```bash
docker build -t spam-api:multistage .
minikube image load spam-api:multistage
cd q4-deployment
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl port-forward svc/spam-api 8080:80
```

Self-healing demo: `kubectl delete pod <name>`, then `kubectl get pods` shows a fresh
replacement pod under the same ReplicaSet within seconds. Rolling update demo: bump the
app version, rebuild as a new tag, then
`kubectl set image deployment/spam-api spam-api=spam-api:<new-tag>` and watch
`kubectl rollout status` / `kubectl rollout history`. See `evidence/q4-deployment/`.

## Report and evidence

`reportDA3408A2.pdf` contains the full written answers to all four questions. `evidence/`
contains the screenshots and terminal logs each answer refers back to, organized by
question — see `evidence/README.md` for what's in each folder.

## Video walkthrough

[Video explanation](https://drive.google.com/file/d/1a3Aq4FjUKZrFHj7DJPsM4j68eWk3j32Z/view?usp=drive_link)

## AI disclosure

See `AI_DISCLOSURE.md`.
