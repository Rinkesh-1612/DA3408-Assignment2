import csv
import os

INDEX = int(os.environ["JOB_COMPLETION_INDEX"])
POD_NAME = os.environ.get("POD_NAME", "unknown-pod")
NODE_NAME = os.environ.get("NODE_NAME", "unknown-node")

SHARD_PATH = f"shards/shard-{INDEX}.csv"


def is_invalid(row):
    name = row["name"].strip()
    email = row["email"].strip()
    if not name or not email:
        return True
    if "@" not in email:
        return True
    return False


def main():
    total = 0
    invalid_count = 0
    with open(SHARD_PATH, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            total += 1
            if is_invalid(row):
                invalid_count += 1

    print(
        f"RESULT shard_index={INDEX} pod={POD_NAME} node={NODE_NAME} "
        f"total_rows={total} invalid_rows={invalid_count}"
    )


if __name__ == "__main__":
    main()
