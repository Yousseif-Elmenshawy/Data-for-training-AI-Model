# Contributing to PHP AI Dataset

Thanks for helping improve the dataset! Contributions of all sizes are welcome:
fixing a typo, correcting an expected output, adding new records, or proposing
schema changes.

## Ways to contribute

- 🐞 **Report a problem** — open an Issue describing the record id, what is wrong,
  and what it should be.
- ➕ **Add records** — see the workflow below.
- ⭐ **Review quality** — comment on whether a "common mistake" is realistic or a
  difficulty label fits.
- 🧩 **Suggest schema changes** — open an Issue first so we can discuss before code.

## Ground rules

- Every record must be **original**, written for this project. Do not copy from
  GitHub, Stack Overflow, blogs or other datasets.
- Target **PHP 8.x** and core PHP (the standard library, OOP, PDO, etc.). Avoid
  making the dataset framework-specific.
- Keep each record focused on **one** concept.
- Be honest: if a field does not apply, use `null` — do not invent data.

## Adding or editing records

Content lives in the topic modules under `scripts/`:

```text
scripts/_data_php_basics.py
scripts/_data_variables.py
scripts/_data_conditions.py
scripts/_data_loops.py
scripts/_data_arrays_strings.py
scripts/_data_functions.py
scripts/_data_forms_input.py
scripts/_data_exceptions.py
scripts/_data_oop.py
scripts/_data_files_json.py
scripts/_data_sessions_auth.py
scripts/_data_pdo_mysql.py
scripts/_data_rest_api.py
scripts/_data_security.py
scripts/_data_testing.py
```

Each file exposes a list of **9-tuples**:

```python
(task_type, difficulty, prompt, code, expected_output,
 explanation, common_mistake, corrected_code, test_case)
```

Example:

```python
("code_generation", "beginner",
 "Write a function that returns the sum of two integers with type declarations.",
 "<?php\nfunction add(int $a, int $b): int {\n    return $a + $b;\n}\necho add(2, 3);",
 "5",
 "Parameter and return type declarations document the contract and enforce it at call time.",
 "Omitting the return type and letting PHP infer, which hides intent.",
 None,
 "assertEquals(5, add(2, 3));"),
```

### Field guidance

- `task_type`: one of `code_generation`, `code_explanation`, `find_bug`,
  `predict_output`, `code_review`, `refactoring`, `code_completion`,
  `write_test`, `explain_error`, `security_improvement`, `conversion`.
- `difficulty`: `beginner`, `intermediate` or `advanced`.
- `prompt`: must be **unique** across the whole dataset. Avoid bare
  "What does this print?" — make it specific to the snippet.
- `explanation`: explain _why_, not a restatement of the code.
- `common_mistake`: a real, plausible mistake (or `null` if none fits).
- `corrected_code`: provide it for `find_bug`, `refactoring`,
  `security_improvement` and `explain_error` records.
- `test_case`: a short assertion or hint, or `null`.

### Changing the number of records

The validator enforces the per-topic counts and a 500 total. If you add records,
update the expected counts in **both** `scripts/generate_dataset.py`
(`TOPIC_GROUPS`) and `scripts/validate_dataset.py` (`EXPECTED_COUNTS`), and the
tables in `README.md` and `DATASET_CARD.md`.

## Regenerate and validate before opening a PR

```bash
python scripts/generate_dataset.py
python scripts/validate_dataset.py
python scripts/statistics.py
```

The validator must end with `Status: PASS`. Fix any reported duplicate prompts,
duplicate code, missing fields or distribution mismatches before submitting.

## Pull request checklist

- [ ] Records are original and PHP 8.x.
- [ ] Prompts are unique and specific.
- [ ] `corrected_code` provided where the task requires it.
- [ ] `python scripts/generate_dataset.py` ran cleanly.
- [ ] `python scripts/validate_dataset.py` reports `PASS`.
- [ ] README/DATASET_CARD tables updated if counts changed.

## Code of conduct

Be respectful and constructive. The goal is a dataset people can trust — accuracy
and honesty matter more than volume.
