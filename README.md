# BorgBackup Testing Contribution

## Repository Information

**GitHub Repository:** [https://github.com/GitGuru2003/borg/tree/main](https://github.com/GitGuru2003/borg/tree/main)

**Original Project:** [https://github.com/borgbackup/borg](https://github.com/borgbackup/borg)

---

## Overview

This repository contains my testing contribution to the BorgBackup project.
I added new tests to the BorgBackup test suite to validate the behavior of five important archiver commands. The primary goal was to exercise previously untested code paths, with a particular focus on **error handling**, **safety checks**, and **edge-case behavior**.

These additions improve confidence in command correctness and help prevent regressions in a safety-critical backup system.

### Coverage Improvements

* `benchmark_cmd.py`: 57% → 100% (+43%)
* `lock_cmds.py`: 74% → 100% (+26%)
* `check_cmd.py`: 85% → 100% (+15%)
* `debug_cmd.py`: 78% → 96% (+18%)
* `create_cmd.py`: 82% → 83% (+1%)

---

## Files Modified

This contribution **only adds tests** and does **not modify any production backup code**.

---

### 1. `src/borg/testsuite/archiver/benchmark_cmd_test.py`

**Tests Added:**

* `test_benchmark_crud_info_progress_logjson_lockwait()` – Verifies that multiple global options (`--info`, `--progress`, `--log-json`, `--lock-wait`) can be used together
* `test_benchmark_crud_remote_options()` – Verifies remote execution using `--rsh` and `--remote-path`
* `test_benchmark_crud_full_tests()` – Verifies full benchmark execution when not in test mode
* `test_benchmark_cpu()` – Verifies the CPU benchmark command

**Behavior Validated:**

* Remote execution via SSH
* Compatibility of multiple global options
* Correct execution of CPU benchmarks
* Successful execution of full benchmark workflows

---

### 2. `src/borg/testsuite/archiver/check_cmd_test.py`

**Tests Added:**

* `test_check_repository_only_conflicts()` – Ensures `--repository-only` conflicts with archive-related options
* `test_check_repository_only_find_lost_archives_conflict()` – Ensures `--repository-only` conflicts with `--find-lost-archives`
* `test_check_repair_max_duration_conflict()` – Ensures `--repair` cannot be combined with `--max-duration`
* `test_check_max_duration_requires_repository_only()` – Ensures `--max-duration` requires `--repository-only`

**Behavior Validated:**

* Rejection of unsafe or contradictory option combinations
* Clear error reporting for invalid command usage
* Protection against dangerous repository maintenance operations

---

### 3. `src/borg/testsuite/archiver/create_cmd_test.py`

**Tests Added:**

* `test_create_read_special_fifo_direct()` – Verifies correct archiving of FIFO contents using `--read-special`
* `test_create_read_special_symlink_to_fifo_content()` – Verifies handling of symlinks pointing to FIFOs
* `test_create_read_special_char_device()` – Verifies behavior when archiving character devices

**Behavior Validated:**

* Correct handling of platform-specific special files
* Accurate preservation of streamed file contents
* Correct behavior across supported operating systems

**Note:** These tests are conditionally skipped on unsupported platforms.

---

### 4. `src/borg/testsuite/archiver/debug_cmds_test.py`

**Tests Added:**

* `test_debug_search_repo_objs()` – Verifies searching repository objects using `str:` and `hex:` patterns
* `test_debug_search_repo_objs_invalid_pattern()` – Verifies rejection of invalid search patterns
* `test_debug_get_obj_invalid_id()` – Verifies error handling for invalid object IDs
* `test_debug_parse_obj_invalid_id()` – Verifies safe failure for invalid parse-obj input
* `test_debug_put_obj_invalid_id()` – Verifies safe failure for invalid put-obj input
* `test_debug_get_obj_not_found()` – Verifies handling of missing repository objects

**Behavior Validated:**

* Input validation for debug commands
* Clear and safe failure modes
* Prevention of misuse with malformed object identifiers

---

### 5. `src/borg/testsuite/archiver/lock_cmds_test.py`

**Tests Added:**

* `test_with_lock_successful_command()` – Verifies successful command execution under a repository lock
* `test_with_lock_subprocess_failure_inproc()` – Verifies safe handling of subprocess failures while holding a lock

**Behavior Validated:**

* Correct acquisition and release of repository locks
* Proper cleanup after failures
* Propagation of meaningful error messages

---

## How to Run the Tests

### Prerequisites

Clone the repository and enter the project directory:

```bash
git clone https://github.com/GitGuru2003/borg.git
cd borg
```

Create and activate a virtual environment:

```bash
python3 -m venv borg-env
source borg-env/bin/activate  # Windows: borg-env\Scripts\activate
```

Install development dependencies:

```bash
pip install -r requirements.d/development.txt
pip install -e .
```

Install `fakeroot` (required for some tests):

**macOS**

```bash
brew install fakeroot
```

**Linux**

```bash
sudo apt-get install fakeroot
```

---

### Running All Archiver Tests

```bash
fakeroot -u pytest src/borg/testsuite/archiver -v
```

### Running Tests by Command

```bash
fakeroot -u pytest src/borg/testsuite/archiver/benchmark_cmd_test.py -v
fakeroot -u pytest src/borg/testsuite/archiver/check_cmd_test.py -v
fakeroot -u pytest src/borg/testsuite/archiver/create_cmd_test.py -v
fakeroot -u pytest src/borg/testsuite/archiver/debug_cmds_test.py -v
fakeroot -u pytest src/borg/testsuite/archiver/lock_cmds_test.py -v
```

### Running a Single Test

```bash
fakeroot -u pytest src/borg/testsuite/archiver/check_cmd_test.py::test_check_repository_only_conflicts -v
```

Verbose mode example:

```bash
fakeroot -u pytest src/borg/testsuite/archiver/create_cmd_test.py::test_create_read_special_fifo_direct -vv
```

---

## Checking Code Coverage

```bash
fakeroot -u pytest src/borg/testsuite/archiver \
    --cov=borg.archiver \
    --cov-report=html:coverage_html \
    --cov-report=term
```

Open the HTML report:

**macOS**

```bash
open coverage_html/index.html
```

**Linux**

```bash
xdg-open coverage_html/index.html
```

---

## License

See the `LICENSE` file for details.

