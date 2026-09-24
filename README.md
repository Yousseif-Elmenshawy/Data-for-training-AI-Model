# PHP AI Dataset

A hand-authored, open-source dataset of **500 PHP 8.x examples** for training and
evaluating AI models that understand, generate, explain, fix, review, refactor and
test PHP code.

The dataset is designed for **AI/ML engineers, coding-agent developers, researchers
and PHP learners**. Every record was written specifically for this project — nothing
is copied from GitHub, Stack Overflow or any existing dataset.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PHP](https://img.shields.io/badge/PHP-8.x-777bb4.svg)](https://www.php.net/)
[![Records](https://img.shields.io/badge/records-500-blue.svg)](data/php_dataset.jsonl)
[![Validation](https://img.shields.io/badge/validation-PASS-brightgreen.svg)](scripts/validate_dataset.py)

> **Honesty note:** the numbers and status badges above reflect what the included
> scripts actually check on this repository (record count, uniqueness, field
> presence, topic distribution). This dataset has **not** been benchmarked against
> any AI model, and no accuracy or performance claims are made.

---

## What is this project?

A structured PHP instruction dataset with a single JSONL file (plus a JSON array
mirror) where each of the **500 records** carries a prompt, code, expected output,
an explanation, a common mistake, an optional corrected version and a test case.

It is built to support several PHP-centric AI tasks:

- Code Generation
- Code Explanation
- Bug Fixing / Bug Finding
- Code Review
- Code Understanding
- Refactoring
- Testing
- Learning PHP

## Why was it created?

Most public code datasets are large but noisy, mixing many languages and containing
duplicated or auto-scraped snippets. This dataset trades raw size for **curated
quality**: a fixed, auditable set of PHP-only examples with a consistent schema,
a deliberate topic distribution, and a validator you can run yourself.

## What does it contain?

- **500 records**, PHP 8.x only.
- **15 topics** covering the language from basics to PDO, REST APIs and security.
- **11 task types** so the data is not just "prompt → code".
- Fields for expected output, explanations, common mistakes, corrected code and
  tests — see [Schema](#schema).

## Topics

| #   | Topic                              | Records |
| --- | ---------------------------------- | ------: |
| 1   | PHP Basics                         |      60 |
| 2   | Variables & Data Types             |      40 |
| 3   | Conditions                         |      40 |
| 4   | Loops                              |      40 |
| 5   | Arrays & Strings                   |      50 |
| 6   | Functions                          |      40 |
| 7   | Forms & User Input                 |      35 |
| 8   | Error Handling & Exceptions        |      30 |
| 9   | OOP                                |      45 |
| 10  | Files & JSON                       |      25 |
| 11  | Sessions & Authentication Concepts |      20 |
| 12  | PDO & MySQL                        |      40 |
| 13  | REST APIs                          |      15 |
| 14  | Security & Secure Coding           |      10 |
| 15  | Testing & Debugging                |      10 |
|     | **Total**                          | **500** |

## Task types

| Task type            | Records |
| -------------------- | ------: |
| code_generation      |     245 |
| code_explanation     |      93 |
| find_bug             |      68 |
| predict_output       |      48 |
| code_review          |      19 |
| explain_error        |       8 |
| write_test           |       8 |
| security_improvement |       7 |
| refactoring          |       2 |
| code_completion      |       1 |
| conversion           |       1 |

## Schema

Each record has the following fields. Fields that do not apply to a given example
are set to `null` rather than invented.

```json
{
  "id": "php_0001",
  "language": "PHP",
  "php_version": "8.x",
  "topic": "php_basics",
  "task_type": "code_generation",
  "difficulty": "beginner",
  "prompt": "...",
  "code": "...",
  "expected_output": "...",
  "explanation": "...",
  "common_mistake": "...",
  "corrected_code": "...",
  "test_case": "..."
}
```

- `difficulty` is one of `beginner`, `intermediate`, `advanced`.
- `corrected_code` is populated mainly for `find_bug`, `refactoring`,
  `security_improvement` and `explain_error` records.

## Files

```text
php-ai-dataset/
├── data/
│   ├── php_dataset.jsonl      # 500 records, one JSON object per line
│   └── php_dataset.json       # the same 500 records as a JSON array
├── samples/
│   └── sample_50.jsonl        # first 50 records, for a quick look
├── scripts/
│   ├── generate_dataset.py    # rebuilds data/ and samples/ from the topic modules
│   ├── validate_dataset.py    # runs the validation report
│   ├── statistics.py          # prints dataset statistics
│   └── _data_*.py             # the hand-authored topic content
├── README.md
├── DATASET_CARD.md
├── CONTRIBUTING.md
├── LICENSE
└── .gitignore
```

## Loading the dataset

Python:

```python
import json

records = []
with open("data/php_dataset.jsonl", encoding="utf-8") as fh:
    for line in fh:
        line = line.strip()
        if line:
            records.append(json.loads(line))

print(len(records))          # 500
print(records[0]["topic"])   # php_basics
```

Or as a JSON array:

```python
import json
records = json.load(open("data/php_dataset.json", encoding="utf-8"))
```

Hugging Face `datasets` (once you publish the file):

```python
from datasets import load_dataset
ds = load_dataset("json", data_files="data/php_dataset.jsonl", split="train")
```

## Running the validation

```bash
python scripts/validate_dataset.py
```

Expected report:

```text
Dataset Validation
------------------
Records: 500
Duplicate IDs: 0
Duplicate Prompts: 0
Duplicate Code Snippets: 0
Missing Fields: 0
Empty Required Fields: 0
Invalid Difficulty: 0
Invalid JSON: 0
ID Sequence OK: yes
Topic Distribution OK: yes
Task Types (distinct): 11
JSON Array OK: yes
Status: PASS
```

## Running the statistics

```bash
python scripts/statistics.py
```

Prints record counts per topic, difficulty and task type, plus approximate code
line counts and word counts for prompts and explanations.

## Rebuilding the data

The `data/` and `samples/` files are generated from the hand-authored modules in
`scripts/`:

```bash
python scripts/generate_dataset.py
python scripts/validate_dataset.py
```

## Suggested uses

- Supervised fine-tuning / instruction tuning for PHP assistants.
- Evaluation prompts for code-generation and bug-fixing agents.
- Retrieval-augmented generation over PHP examples.
- A reference for building a PHP coding assistant's test suite.
- Teaching material for PHP 8.x, especially the "common mistake" field.

### Real example: using a record as an instruction

```python
import json

with open("data/php_dataset.jsonl", encoding="utf-8") as fh:
    records = [json.loads(l) for l in fh if l.strip()]

bug = next(r for r in records if r["task_type"] == "find_bug")
print(bug["prompt"])
print(bug["code"])
print("-> fix:", bug["corrected_code"])
```

You can build an instruction/answer pair from any record, for example
`{"instruction": record["prompt"], "input": record["code"], "output": record["corrected_code"]}`.

## Feedback Wanted

This dataset improves with review from the people who know PHP and ML best.
**PHP developers, AI engineers and ML researchers are warmly invited to:**

- 🐞 **Find mistakes** — incorrect expected outputs, wrong explanations, or PHP
  that would not actually run.
- ➕ **Suggest new records** — especially for under-represented task types
  (`refactoring`, `code_completion`, `conversion`) and topics.
- ⭐ **Assess example quality** — is a "common mistake" realistic? Is the
  difficulty label right?
- 🧩 **Propose schema improvements** — new fields, better naming, clearer types.
- 🔀 **Open Issues and Pull Requests** — see [CONTRIBUTING.md](CONTRIBUTING.md).

Every accepted fix makes the dataset more trustworthy for everyone.

## Limitations

- **PHP only.** No other languages are included.
- **Snippets, not applications.** Examples are small and self-contained; they do
  not represent full project structure or framework usage (deliberately, to keep
  the focus on core PHP).
- **No model benchmarks.** Nothing here has been scored against an AI model.
- **Not exhaustive.** 500 records cannot cover every PHP feature or edge case.
- **English prompts.** Prompts and explanations are in English.
- **Reviewed by humans, not formally audited.** Examples are authored and checked
  by hand; there may still be subtle errors. Please report them.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to add or fix records and how to run
the validator before opening a pull request.

## License

Released under the [MIT License](LICENSE).
