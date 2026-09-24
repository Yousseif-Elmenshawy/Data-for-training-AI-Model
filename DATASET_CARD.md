# Dataset Card: PHP AI Dataset

## Dataset Summary

**PHP AI Dataset** is a hand-authored collection of **500 PHP 8.x records** built to
train and evaluate AI models on PHP-specific software engineering tasks. Each record
contains a natural-language prompt, an associated code snippet, an expected output,
an explanation, a common mistake, an optional corrected code snippet and a test case.

- **Language:** PHP 8.x
- **Size:** 500 records (single JSONL file, plus a JSON array mirror)
- **Format:** JSON Lines (`data/php_dataset.jsonl`) and JSON (`data/php_dataset.json`)
- **License:** MIT
- **Created for:** code generation, explanation, bug fixing, code review,
  refactoring, testing and PHP learning.

All examples were written for this project and are not copied from GitHub, Stack
Overflow or any existing dataset.

## Intended Use

- Instruction tuning and fine-tuning of code LLMs and coding agents for PHP.
- Evaluation prompts for PHP code generation, bug localization and review.
- Retrieval-augmented generation (RAG) over PHP examples.
- Educational material and reference tests for PHP assistants.

## Out-of-Scope Use

- **Not** a benchmark with published accuracy numbers — no model has been scored on it.
- **Not** suitable as production code — examples are teaching snippets, some of which
  intentionally contain bugs.
- **Not** a substitute for a security audit — security examples are educational and
  defensive only.
- **Not** multilingual — PHP only.
- **Not** a source of large-scale, real-world code — it favors clarity over scale.

## Dataset Structure

Each record is a JSON object:

| Field             | Type           | Description                                        |
| ----------------- | -------------- | -------------------------------------------------- |
| `id`              | string         | Unique id, `php_0001` … `php_0500`.                |
| `language`        | string         | Always `"PHP"`.                                    |
| `php_version`     | string         | Always `"8.x"`.                                    |
| `topic`           | string         | One of the 15 topic slugs.                         |
| `task_type`       | string         | One of the task-type slugs (see below).            |
| `difficulty`      | string         | `beginner`, `intermediate` or `advanced`.          |
| `prompt`          | string         | The instruction / question.                        |
| `code`            | string \| null | The PHP snippet (present for all current records). |
| `expected_output` | string \| null | Expected program output or answer.                 |
| `explanation`     | string         | Why the code behaves as it does.                   |
| `common_mistake`  | string \| null | A realistic mistake and how to avoid it.           |
| `corrected_code`  | string \| null | Fixed code for bug/refactor/security examples.     |
| `test_case`       | string \| null | A short assertion or test hint.                    |

Splits: the dataset ships as a single set. The file `samples/sample_50.jsonl` offers
the first 50 records for quick inspection. Users should create their own splits.

Topics (counts): php_basics 60, variables 40, conditions 40, loops 40,
arrays_strings 50, functions 40, forms_input 35, exceptions 30, oop 45,
files_json 25, sessions_auth 20, pdo_mysql 40, rest_api 15, security 10,
testing 10.

Task types (counts): code_generation 245, code_explanation 93, find_bug 68,
predict_output 48, code_review 19, explain_error 8, write_test 8,
security_improvement 7, refactoring 2, code_completion 1, conversion 1.

## Data Creation Process

1. Topics and per-topic record counts were fixed up front (see the README table).
2. Each record was authored by hand around a single concrete PHP concept, with a
   realistic prompt and a realistic mistake.
3. Content lives in small Python modules (`scripts/_data_*.py`) as 9-field rows.
4. `scripts/generate_dataset.py` assembles the rows into the JSONL/JSON files and
   assigns `php_0001` … `php_0500` ids in topic order.
5. `scripts/validate_dataset.py` checks counts, uniqueness, fields and distribution.

No web scraping and no generated code from other models were used.

## Quality Control

- **Automated validation** (`scripts/validate_dataset.py`) enforces:
  - exactly 500 records,
  - unique ids in the exact `php_0001`…`php_0500` range,
  - presence of all required fields and non-empty core text fields,
  - no duplicate prompts,
  - no clearly duplicate code snippets,
  - the exact topic distribution,
  - valid difficulty values,
  - JSON/JSONL consistency.
- **Manual authoring** with a single concept per record and a deliberate common
  mistake, plus corrected code wherever the task is bug/refactor/security oriented.

The validator passing means the _structural_ rules hold. It does **not** prove that
every snippet is semantically perfect — human review is requested (see README).

## Limitations

- Small and curated: 500 records is not a large-scale corpus.
- Core-PHP focused; placeholder-based code (e.g. `$pdo`, `$user`) rather than runnable
  full applications.
- English prompts only.
- Some snippets are intentionally buggy (bug-finding records) — do not run blindly.
- Human-reviewed but not formally audited; subtle errors may remain.

## License

MIT License. See [LICENSE](../LICENSE). The license applies to the dataset content
and the scripts in this repository.

## Ethical Considerations

- **Security examples are defensive.** Injection, XSS and password-handling records
  show the vulnerable pattern _and_ the safe fix, for teaching purposes.
- **No personal data.** The dataset contains no real user data, credentials or PII.
- **No harmful capabilities.** Examples are educational PHP; none are intended to
  facilitate attacks against real systems.

## Bias Considerations

- Content reflects common PHP teaching patterns and web-development idioms, so it may
  under-represent niche domains (CLI tooling, embedded, exotic extensions).
- Difficulty labels are the authors' judgment and may be subjective.
- Examples favor the procedural + PDO/MySQL style over framework-heavy code; this is
  intentional (framework-agnostic core PHP) but is itself a bias.
- Prompts assume an English-speaking learner.

## Maintenance

- Structural checks are automated and can be re-run any time.
- Corrections and additions are welcome via Issues and Pull Requests; see
  [CONTRIBUTING.md](../CONTRIBUTING.md).
- When editing content, regenerate and re-validate:

  ```bash
  python scripts/generate_dataset.py
  python scripts/validate_dataset.py
  ```

- The dataset is versioned in the repository; breaking schema changes will be noted
  in the README and this card.
