# Evidence

Terminal output backing each question. Text captures were taken from the live cluster and
local docker. Screenshots cover the runs that are no longer reproducible from the current
cluster state.

## q1-image-sizes

- `image-sizes.txt` shows both tags side by side. naive 1.59GB, multistage 513MB, so a
  67.7% reduction.

Screenshots still to add here: the two `docker build` runs, and the containers answering
`/healthz` and `/predict` for each tag.

## q2-compose-cache

Nothing captured live. The compose stack was brought down, so the timings have to come
from the screenshots.

Screenshots to add: `docker compose up --build` with both services attached, and the
`CACHE MISS 29.45ms` / `CACHE HIT 0.35ms` pair from the api container logs.

## q3-indexed-job

- `pods-and-job.txt` shows all 8 pods Completed and the job at 8/8, with the node each
  pod landed on.
- `shard-results.txt` has all 8 RESULT lines read back through `kubectl logs`. Counts are
  10, 15, 10, 8, 6, 9, 13, 11 and match what `generate_shards.py` seeded.

Screenshot still needed: the `kubectl get pods -o wide` taken while the job was running.
That one matters more than the file above. The captured file shows every pod at 25h old
because the job finished a day ago, which proves the job completed but not that
parallelism 4 was ever actually reached. The screenshot showing 4 pods Completed at 16s
with the next 4 at 8s is the only thing that proves concurrency, and the rubric asks for
exactly that.

## q4-deployment

- `deployment-and-rollout.txt` has the Deployment at 2/2, the Service, both ReplicaSets
  with the old one scaled to 0, `rollout status`, and `rollout history` showing revisions
  1 and 2.

Screenshots to add: the pod delete and its automatic replacement, the live `rollout
status` progress lines, and `/healthz` returning `{"status":"ok","version":"v2"}`.

The self-healing demo ran against ReplicaSet 77f4dcbc9b, before the rolling update. Every
pod from that ReplicaSet has since been replaced, so the recreation cannot be seen in the
cluster now and the screenshot is the only record of it.
