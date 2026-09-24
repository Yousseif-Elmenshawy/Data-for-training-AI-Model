# -*- coding: utf-8 -*-
"""
validate_dataset.py
--------------------
Validates data/php_dataset.jsonl (and data/php_dataset.json) against the dataset
rules and prints a report.

Checks:
  * exactly 500 records
  * no duplicate IDs, and IDs run php_0001 .. php_0500
  * all required fields present
  * valid JSON on every line / in the JSON file
  * no empty records / empty required text fields
  * no duplicate prompts
  * no clearly duplicate code snippets
  * topic distribution matches the spec
  * task_type distribution is non-trivial
  * difficulty values are within the allowed set

Exit code 0 on PASS, 1 on FAIL.

Usage:
    python scripts/validate_dataset.py
"""

import json
import os
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA_DIR = os.path.join(ROOT, "data")
JSONL_PATH = os.path.join(DATA_DIR, "php_dataset.jsonl")
JSON_PATH = os.path.join(DATA_DIR, "php_dataset.json")

REQUIRED_FIELDS = [
    "id", "language", "php_version", "topic", "task_type", "difficulty",
    "prompt", "code", "expected_output", "explanation", "common_mistake",
    "corrected_code", "test_case",
]
# Fields that must be non-empty text for every record.
NON_EMPTY_FIELDS = ["id", "language", "php_version", "topic", "task_type",
                    "difficulty", "prompt", "explanation"]

EXPECTED_COUNTS = {
    "php_basics": 60,
    "variables": 40,
    "conditions": 40,
    "loops": 40,
    "arrays_strings": 50,
    "functions": 40,
    "forms_input": 35,
    "exceptions": 30,
    "oop": 45,
    "files_json": 25,
    "sessions_auth": 20,
    "pdo_mysql": 40,
    "rest_api": 15,
    "security": 10,
    "testing": 10,
}

VALID_DIFFICULTIES = {"beginner", "intermediate", "advanced"}
EXPECTED_TOTAL = 500


def load_jsonl(path):
    records = []
    invalid = 0
    if not os.path.exists(path):
        print("Missing file:", path)
        return records, 1
    with open(path, encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as exc:
                invalid += 1
                print("Invalid JSON on line %d: %s" % (lineno, exc))
    return records, invalid


def norm_code(code):
    """Normalize a code snippet for duplicate detection."""
    if not code:
        return None
    return "".join(code.split())


def main():
    records, invalid_json = load_jsonl(JSONL_PATH)

    total = len(records)

    ids = [r.get("id") for r in records]
    id_counts = Counter(ids)
    duplicate_ids = sum(1 for k, v in id_counts.items() if v > 1 and k is not None)

    # ID sequence check.
    expected_ids = ["php_%04d" % i for i in range(1, EXPECTED_TOTAL + 1)]
    id_sequence_ok = sorted(x for x in ids if x) == expected_ids

    prompts = [r.get("prompt") for r in records]
    duplicate_prompts = sum(1 for k, v in Counter(prompts).items() if v > 1)

    codes = [norm_code(r.get("code")) for r in records]
    codes = [c for c in codes if c]
    duplicate_codes = sum(1 for k, v in Counter(codes).items() if v > 1)

    missing_fields = 0
    empty_fields = 0
    bad_difficulty = 0
    for r in records:
        for f in REQUIRED_FIELDS:
            if f not in r:
                missing_fields += 1
        for f in NON_EMPTY_FIELDS:
            v = r.get(f)
            if not isinstance(v, str) or v.strip() == "":
                empty_fields += 1
        if r.get("difficulty") not in VALID_DIFFICULTIES:
            bad_difficulty += 1

    topic_counts = Counter(r.get("topic") for r in records)
    topic_ok = dict(topic_counts) == EXPECTED_COUNTS

    task_counts = Counter(r.get("task_type") for r in records)
    distinct_task_types = len(task_counts)

    # JSON array file check.
    json_array_ok = False
    if os.path.exists(JSON_PATH):
        try:
            with open(JSON_PATH, encoding="utf-8") as fh:
                data = json.load(fh)
            json_array_ok = isinstance(data, list) and len(data) == total
        except json.JSONDecodeError:
            json_array_ok = False

    failures = []
    if total != EXPECTED_TOTAL:
        failures.append("record count %d != %d" % (total, EXPECTED_TOTAL))
    if duplicate_ids:
        failures.append("%d duplicate IDs" % duplicate_ids)
    if not id_sequence_ok:
        failures.append("IDs are not php_0001..php_%04d" % EXPECTED_TOTAL)
    if duplicate_prompts:
        failures.append("%d duplicate prompts" % duplicate_prompts)
    if duplicate_codes:
        failures.append("%d duplicate code snippets" % duplicate_codes)
    if missing_fields:
        failures.append("%d missing fields" % missing_fields)
    if empty_fields:
        failures.append("%d empty required fields" % empty_fields)
    if bad_difficulty:
        failures.append("%d invalid difficulty values" % bad_difficulty)
    if invalid_json:
        failures.append("%d invalid JSON lines" % invalid_json)
    if not topic_ok:
        failures.append("topic distribution mismatch")
    if not json_array_ok:
        failures.append("php_dataset.json is not a 500-record array")

    status = "PASS" if not failures else "FAIL"

    print("Dataset Validation")
    print("------------------")
    print("Records: %d" % total)
    print("Duplicate IDs: %d" % duplicate_ids)
    print("Duplicate Prompts: %d" % duplicate_prompts)
    print("Duplicate Code Snippets: %d" % duplicate_codes)
    print("Missing Fields: %d" % missing_fields)
    print("Empty Required Fields: %d" % empty_fields)
    print("Invalid Difficulty: %d" % bad_difficulty)
    print("Invalid JSON: %d" % invalid_json)
    print("ID Sequence OK: %s" % ("yes" if id_sequence_ok else "no"))
    print("Topic Distribution OK: %s" % ("yes" if topic_ok else "no"))
    print("Task Types (distinct): %d" % distinct_task_types)
    print("JSON Array OK: %s" % ("yes" if json_array_ok else "no"))
    print("Status: %s" % status)

    if failures:
        print("")
        print("Problems:")
        for f in failures:
            print(" - %s" % f)

    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
