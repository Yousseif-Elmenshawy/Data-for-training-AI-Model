# -*- coding: utf-8 -*-
"""
statistics.py
--------------
Prints statistics about data/php_dataset.jsonl:

  * number of records
  * records per topic
  * records per difficulty
  * records per task type
  * approximate number of code lines
  * word counts for prompts and explanations

Usage:
    python scripts/statistics.py
"""

import json
import os
import sys
from collections import Counter, OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
JSONL_PATH = os.path.join(ROOT, "data", "php_dataset.jsonl")

TOPIC_ORDER = [
    "php_basics", "variables", "conditions", "loops", "arrays_strings",
    "functions", "forms_input", "exceptions", "oop", "files_json",
    "sessions_auth", "pdo_mysql", "rest_api", "security", "testing",
]


def load(path):
    records = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def bar(n, width=40, scale=1.0):
    return "#" * int(round(n * scale)) + (" " * 0) if n else ""


def main():
    if not os.path.exists(JSONL_PATH):
        print("Missing:", JSONL_PATH)
        return 1

    records = load(JSONL_PATH)
    total = len(records)

    print("PHP AI Dataset Statistics")
    print("=========================")
    print("Total records: %d" % total)
    print("")

    # Records per topic (in spec order).
    topic_counts = Counter(r["topic"] for r in records)
    print("Records per topic")
    print("-----------------")
    max_topic = max(topic_counts.values()) if topic_counts else 1
    for topic in TOPIC_ORDER:
        c = topic_counts.get(topic, 0)
        scale = 30.0 / max_topic
        print("  %-15s %3d  %s" % (topic, c, "#" * int(round(c * scale))))
    print("")

    # Records per difficulty.
    diff_counts = Counter(r["difficulty"] for r in records)
    print("Records per difficulty")
    print("----------------------")
    for d in ["beginner", "intermediate", "advanced"]:
        print("  %-13s %3d" % (d, diff_counts.get(d, 0)))
    print("")

    # Records per task type.
    task_counts = Counter(r["task_type"] for r in records)
    print("Records per task type")
    print("---------------------")
    for t, c in sorted(task_counts.items(), key=lambda kv: (-kv[1], kv[0])):
        print("  %-22s %3d" % (t, c))
    print("")

    # Approximate code lines.
    code_lines = 0
    corrected_lines = 0
    for r in records:
        if r.get("code"):
            code_lines += len(r["code"].splitlines())
        if r.get("corrected_code"):
            corrected_lines += len(r["corrected_code"].splitlines())
    print("Approximate code lines")
    print("----------------------")
    print("  code lines:            %d" % code_lines)
    print("  corrected_code lines:  %d" % corrected_lines)
    print("  total:                 %d" % (code_lines + corrected_lines))
    print("")

    # Word counts.
    prompt_words = sum(len((r.get("prompt") or "").split()) for r in records)
    expl_words = sum(len((r.get("explanation") or "").split()) for r in records)
    print("Word counts")
    print("-----------")
    print("  prompt words:      %d (avg %.1f/record)" %
          (prompt_words, prompt_words / total if total else 0))
    print("  explanation words: %d (avg %.1f/record)" %
          (expl_words, expl_words / total if total else 0))
    print("")

    # Field completeness.
    fields = ["code", "expected_output", "explanation", "common_mistake",
              "corrected_code", "test_case"]
    print("Field completeness (non-null)")
    print("-----------------------------")
    for f in fields:
        present = sum(1 for r in records if r.get(f) is not None)
        print("  %-16s %3d/%d" % (f, present, total))

    return 0


if __name__ == "__main__":
    sys.exit(main())
