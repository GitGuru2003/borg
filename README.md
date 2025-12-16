# BorgBackup Testing Contribution

## Repository Information

**GitHub Repository:** https://github.com/GitGuru2003/borg/tree/main

**Original Project:** https://github.com/borgbackup/borg

---

## Overview

I added a bunch of new tests to BorgBackup to check if five important archiver commands work correctly. The main goal was to test parts of the code that weren't covered before, especially when things go wrong or weird things happen.

### How Much Coverage I Improved

- `benchmark_cmd.py`: 57% → 100% (added 43%)
- `lock_cmds.py`: 74% → 100% (added 26%)
- `check_cmd.py`: 85% → 100% (added 15%)
- `debug_cmd.py`: 78% → 96% (added 18%)
- `create_cmd.py`: 82% → 83% (added 1%)

---

## Files Modified

I only added tests - didn't change any of the actual backup code.

### 1. `src/borg/testsuite/archiver/benchmark_cmd_test.py`

**Tests I Added:**

- `test_benchmark_crud_info_progress_logjson_lockwait()` - Tests if you can use multiple options together like --info, --progress, --log-json, and --lock-wait
- `test_benchmark_crud_remote_options()` - Tests if the backup works when you use --rsh and --remote-path for remote backups
- `test_benchmark_crud_full_tests()` - Tests if the full benchmark works when it's not in test mode
- `test_benchmark_cpu()` - Tests the CPU benchmark feature

**What Gets Tested:**

- Can it backup to a remote server using SSH?
- Do all the options work together?
- Does CPU benchmarking work?
- Does the full benchmark run correctly?

---

### 2. `src/borg/testsuite/archiver/check_cmd_test.py`

**Tests I Added:**

- `test_check_repository_only_conflicts()` - Makes sure you can't use --repository-only with archive options at the same time
- `test_check_repository_only_find_lost_archives_conflict()` - Checks that --repository-only and --find-lost-archives can't be used together
- `test_check_repair_max_duration_conflict()` - Makes sure you can't use --repair and --max-duration at the same time
- `test_check_max_duration_requires_repository_only()` - Checks that --max-duration only works if you also use --repository-only

**What Gets Tested:**

- Does it stop you from using dangerous options together?
- Does it catch when you accidentally use conflicting options?
- Is the user protected from messing things up?

---

### 3. `src/borg/testsuite/archiver/create_cmd_test.py`

**Tests I Added:**

- `test_create_read_special_fifo_direct()` - Tests if it can backup special pipe files with --read-special
- `test_create_read_special_symlink_to_fifo_content()` - Tests if it handles links that point to pipes
- `test_create_read_special_char_device()` - Tests if it can backup character devices

**What Gets Tested:**

- Can it handle weird special files on Linux/macOS?
- Does it correctly copy data from pipes?
- Does it work on different operating systems?
- Does the backup preserve the data correctly?

**Note:** These tests skip if they're running on incompatible systems

---

### 4. `src/borg/testsuite/archiver/debug_cmds_test.py`

**Tests I Added:**

- `test_debug_search_repo_objs()` - Tests if you can search for files using hex codes or text
- `test_debug_search_repo_objs_invalid_pattern()` - Tests if it rejects bad search patterns
- `test_debug_get_obj_invalid_id()` - Tests if it gives an error when you ask for a file with a bad ID
- `test_debug_parse_obj_invalid_id()` - Tests if parse-obj doesn't break with a bad ID
- `test_debug_put_obj_invalid_id()` - Tests if put-obj doesn't break with a bad ID
- `test_debug_get_obj_not_found()` - Tests if it handles missing files properly

**What Gets Tested:**

- Does it check if the search pattern is valid before searching?
- Does it give helpful errors when things go wrong?
- Does it prevent you from using bad file IDs?
- Does it handle things gracefully when a file doesn't exist?

---

### 5. `src/borg/testsuite/archiver/lock_cmds_test.py`

**Tests I Added:**

- `test_with_lock_successful_command()` - Tests if a command works when it locks the repository
- `test_with_lock_subprocess_failure_inproc()` - Tests what happens when a command fails while holding the lock

**What Gets Tested:**

- Does it properly lock and unlock the repository?
- What happens if a backup fails, does it clean up properly?
- Does the error message get passed back to the user?

---

## How to Run the Tests

### Prerequisites

First, clone the repository and set it up:

```bash
git clone https://github.com/GitGuru2003/borg.git
cd borg
```

Create a virtual environment:

```bash
python3 -m venv borg-env
source borg-env/bin/activate  # On Windows: borg-env\Scripts\activate
```

Install what you need to run the tests:

```bash
pip install -r requirements.d/development.txt
pip install -e .
```

You'll also need fakeroot to run the tests properly:

**macOS:**
```bash
brew install fakeroot
```

**Linux:**
```bash
sudo apt-get install fakeroot
```

### Running All the Tests

Run everything at once:

```bash
fakeroot -u pytest src/borg/testsuite/archiver -v
```

Or run tests for specific commands:

```bash
fakeroot -u pytest src/borg/testsuite/archiver/benchmark_cmd_test.py -v
fakeroot -u pytest src/borg/testsuite/archiver/check_cmd_test.py -v
fakeroot -u pytest src/borg/testsuite/archiver/create_cmd_test.py -v
fakeroot -u pytest src/borg/testsuite/archiver/debug_cmd_test.py -v
fakeroot -u pytest src/borg/testsuite/archiver/lock_cmds_test.py -v
```

### Running Just One Test

If you want to test just one thing:

```bash
fakeroot -u pytest src/borg/testsuite/archiver/check_cmd_test.py::test_check_repository_only_conflicts -v
```

Or with even more details:

```bash
fakeroot -u pytest src/borg/testsuite/archiver/create_cmd_test.py::test_create_read_special_fifo_direct -vv
```

### Checking Code Coverage

To see how much code gets tested:

```bash
fakeroot -u pytest src/borg/testsuite/archiver \
    --cov=borg.archiver \
    --cov-report=html:coverage_html \
    --cov-report=term
```

Then open the report:

**macOS:**
```bash
open coverage_html/index.html
```

**Linux:**
```bash
xdg-open coverage_html/index.html
```

---

## License

See LICENSE file for details.
