import csv
import os
import random

NUM_SHARDS=8
ROWS_PER_SHARD=50
INVALID_RATE=0.2
FIRST_NAMES=["alice","bob","carol","dave","erin","frank","grace","heidi"]
DOMAINS=["example.com","test.org","mail.co","corp.io"]
os.makedirs("shards",exist_ok=True)

for shard_id in range(NUM_SHARDS):
    rng = random.Random(1000 + shard_id)
    rows = []
    invalid_count = 0

    for i in range(ROWS_PER_SHARD):
        name = rng.choice(FIRST_NAMES)
        domain = rng.choice(DOMAINS)
        is_invalid = rng.random() < INVALID_RATE

        if is_invalid:
            kind = rng.choice(["bad_email", "missing_email", "missing_name"])
            if kind == "bad_email":
                email = f"{name}{i}{domain}"        # no "@" — malformed
            elif kind == "missing_email":
                email = ""                            # missing required field
            else:
                name = ""                             # missing required field
                email = f"{name}{i}@{domain}"
            invalid_count += 1
        else:
            email = f"{name}{i}@{domain}"

        rows.append([i, name, email])

    with open(f"shards/shard-{shard_id}.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "name", "email"])
        writer.writerows(rows)

    print(f"shard-{shard_id}.csv: {invalid_count} invalid rows (seed={1000 + shard_id})")