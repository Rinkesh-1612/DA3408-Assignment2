# Evidence

Terminal output and screenshots backing each question.

## q1-image-sizes

Both Dockerfiles use the same `python:3.12` base (no `-slim`), so the size difference
comes entirely from what the multi-stage build excludes from its final image.


- `q1_naive_build.png`: Single-stage Dockerfile build output and image size (1.59GB).
- `q1_naive_curl.png`: Testing `/healthz` and `POST /predict` endpoints on naive container.
- `q1_multistage.png`: Multi-stage build output, exact image size (1426.7 MiB / 1495960411
  bytes vs naive's 1513.3 MiB / 1586794058 bytes — 5.72% reduction).

## q2-compose-cache

- `q2_compose_up.png`: `docker compose up --build` starting `api` and `cache` services.
- `q2_cache_timing.png`: Logs showing `CACHE MISS` (29.45ms) vs `CACHE HIT` (0.35ms).

## q3-indexed-job

- `pods-and-job.txt`: Output showing all 8 pods Completed and node assignments.
- `shard-results.txt`: Invalid row counts per shard collected via `kubectl logs`.
- `q3_generate_shards.png`: Generating 8 CSV shards with invalid row counts.
- `q3_build_validator.png`: `docker build -t shard-validator:v1 .` image build.
- `q3_pods_wide.png`: `kubectl get pods -o wide` during execution proving `parallelism: 4`.
- `q3_logs.png`: Invalid row counts retrieved across all 8 pods via `kubectl logs`.

## q4-deployment

The Deployment image was rebuilt as `spam-api:multistage-v2b` after the Q1 base-image fix
(dropping `-slim`), so this evidence reflects the corrected Dockerfile. A new tag was used
instead of reusing `multistage-v2` so that `kubectl set image` would trigger a real rollout
(same image string = no diff = no rollout).


- `q4_apply_service.png`: `service.yaml` applied, 2 replicas ready, and ClusterIP service setup.
- `q4_build_v2.png`: `spam-api:multistage-v2b` docker build (corrected base image).
- `q4_rollout_status.png`: `minikube image load`, `kubectl set image`, full `kubectl rollout
  status` transcript, and `kubectl rollout history` showing 3 revisions.
- `q4_curl_and_selfheal.png`: `/healthz` returning `{"status":"ok","version":"v2"}` through
  the rebuilt image, plus pod deletion and the ReplicaSet automatically creating a fresh
  replacement pod.
