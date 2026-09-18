Rinkesh Patel (DA24B017)  

---

For this assignment I used Claude code primarily (Sonnet 5) as aassistant to help with code generation and syntax checking of  configuration  and document formatting. Here is a breakdown of how and where AI was used:

### 1. LaTeX Layout & Page Budgeting (`report.tex`)
- I used AI to help structure and style the LaTeX report so that all technical answers, code listings, and explanations fit cleanly into the strict 2-page limit without overflowing or messing up the document and presentation was clean.

### 2. Shard Generation Script (`q3-data-validation/generate_shards.py`)
- I used AI to write the Python script that generates the 8 CSV data shards. The script splits the signup data and deterministically inserts bad emails and missing fields into 50-row shards so we had proper data to test the Kubernetes Indexed Job.

### 3. Redis Caching & FastAPI Logic (`app/main.py`)
- I used AI to help implement the Redis caching layer in FastAPI (`cache.get`, `cache.setex` with a 300s TTL) and to add execution timing logs so I could measure cache hits vs. misses.

### 4. Docker & Kubernetes Manifests
- I used AI for syntax checking and drafting `docker-compose.yml`, `job.yaml` and the relevant Dockerfiles  becasue  the syntax was really timeconsuming .


---


