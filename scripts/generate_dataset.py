# -*- coding: utf-8 -*-
"""
generate_dataset.py
--------------------
Builds the complete PHP AI Dataset (500 records) from the hand-authored topic
modules in this folder, then writes:

    data/php_dataset.jsonl   (500 lines, one record per line)
    data/php_dataset.json    (JSON array, same 500 records)
    samples/sample_50.jsonl  (first 50 records)

Every record is authored for this project. IDs are assigned in topic order:
php_0001 ... php_0500.

Run from anywhere:
    python scripts/generate_dataset.py
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA_DIR = os.path.join(ROOT, "data")
SAMPLES_DIR = os.path.join(ROOT, "samples")

# Make sibling _data_* modules importable regardless of the working directory.
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import _data_php_basics
import _data_variables
import _data_conditions
import _data_loops
import _data_arrays_strings
import _data_functions
import _data_forms_input
import _data_exceptions
import _data_oop
import _data_files_json
import _data_sessions_auth
import _data_pdo_mysql
import _data_rest_api
import _data_security
import _data_testing

# Ordered topic groups: (topic_name, module, list attribute, expected count).
TOPIC_GROUPS = [
    ("php_basics", _data_php_basics, "BASICS", 60),
    ("variables", _data_variables, "VARIABLES", 40),
    ("conditions", _data_conditions, "CONDITIONS", 40),
    ("loops", _data_loops, "LOOPS", 40),
    ("arrays_strings", _data_arrays_strings, "ARRAYS_STRINGS", 50),
    ("functions", _data_functions, "FUNCTIONS", 40),
    ("forms_input", _data_forms_input, "FORMS_INPUT", 35),
    ("exceptions", _data_exceptions, "EXCEPTIONS", 30),
    ("oop", _data_oop, "OOP", 45),
    ("files_json", _data_files_json, "FILES_JSON", 25),
    ("sessions_auth", _data_sessions_auth, "SESSIONS_AUTH", 20),
    ("pdo_mysql", _data_pdo_mysql, "PDO_MYSQL", 40),
    ("rest_api", _data_rest_api, "REST_API", 15),
    ("security", _data_security, "SECURITY", 10),
    ("testing", _data_testing, "TESTING", 10),
]

FIELD_ORDER = [
    "id", "language", "php_version", "topic", "task_type", "difficulty",
    "prompt", "code", "expected_output", "explanation", "common_mistake",
    "corrected_code", "test_case",
]


def build_records():
    records = []
    counter = 0
    for topic, module, attr, expected in TOPIC_GROUPS:
        rows = getattr(module, attr)
        if len(rows) != expected:
            raise SystemExit(
                "Topic %r has %d records, expected %d" % (topic, len(rows), expected)
            )
        for (task_type, difficulty, prompt, code, expected_output,
             explanation, common_mistake, corrected_code, test_case) in rows:
            counter += 1
            records.append({
                "id": "php_%04d" % counter,
                "language": "PHP",
                "php_version": "8.x",
                "topic": topic,
                "task_type": task_type,
                "difficulty": difficulty,
                "prompt": prompt,
                "code": code,
                "expected_output": expected_output,
                "explanation": explanation,
                "common_mistake": common_mistake,
                "corrected_code": corrected_code,
                "test_case": test_case,
            })
    return records


def ordered(record):
    return {k: record.get(k) for k in FIELD_ORDER}


def main():
    records = build_records()
    if len(records) != 500:
        raise SystemExit("Expected 500 records, got %d" % len(records))

    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(SAMPLES_DIR, exist_ok=True)

    records = [ordered(r) for r in records]

    jsonl_path = os.path.join(DATA_DIR, "php_dataset.jsonl")
    with open(jsonl_path, "w", encoding="utf-8", newline="\n") as fh:
        for r in records:
            fh.write(json.dumps(r, ensure_ascii=False))
            fh.write("\n")

    json_path = os.path.join(DATA_DIR, "php_dataset.json")
    with open(json_path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(records, fh, ensure_ascii=False, indent=2)
        fh.write("\n")

    sample_path = os.path.join(SAMPLES_DIR, "sample_50.jsonl")
    with open(sample_path, "w", encoding="utf-8", newline="\n") as fh:
        for r in records[:50]:
            fh.write(json.dumps(r, ensure_ascii=False))
            fh.write("\n")

    print("Wrote %d records" % len(records))
    print(" - %s" % jsonl_path)
    print(" - %s" % json_path)
    print(" - %s" % sample_path)


if __name__ == "__main__":
    main()
