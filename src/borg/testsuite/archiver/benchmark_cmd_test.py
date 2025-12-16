from ...constants import *  # NOQA
from . import cmd, RK_ENCRYPTION


def test_benchmark_crud(archiver, monkeypatch):
    cmd(archiver, "repo-create", RK_ENCRYPTION)
    monkeypatch.setenv("_BORG_BENCHMARK_CRUD_TEST", "YES")
    cmd(archiver, "benchmark", "crud", archiver.input_path)

# These are the tests I added
# Make sure CRUD benchmark works with all the flags at once
def test_benchmark_crud_info_progress_logjson_lockwait(archiver, monkeypatch):
    cmd(archiver, "repo-create", RK_ENCRYPTION)
    monkeypatch.setenv("_BORG_BENCHMARK_CRUD_TEST", "YES")


    cmd(
        archiver,
        "benchmark",
        "--info",
        "--progress",
        "--log-json",
        "--lock-wait", "10",
        "crud",
        archiver.input_path,
    )

def test_benchmark_cpu(archiver):
    cmd(archiver, "benchmark", "cpu")

# Make sure full benchmark runs when test mode is off
def test_benchmark_crud_full_tests(archiver, monkeypatch):
    """Test that the full benchmark test suite is defined when not in test mode."""

    monkeypatch.delenv("_BORG_BENCHMARK_CRUD_TEST", raising=False)
    
    cmd(archiver, "repo-create", RK_ENCRYPTION)
    cmd(archiver, "benchmark", "crud", archiver.input_path)

def test_benchmark_crud_remote_options(archiver, monkeypatch):
    """Test benchmark crud with --rsh and --remote-path options"""
    cmd(archiver, "repo-create", RK_ENCRYPTION)
    monkeypatch.setenv("_BORG_BENCHMARK_CRUD_TEST", "YES")
    
    
    cmd(archiver, "--rsh", "ssh -o StrictHostKeyChecking=no", "benchmark", "crud", archiver.input_path)
    
    
    cmd(archiver, "--remote-path", "borg", "benchmark", "crud", archiver.input_path)
    
    # Test with both options
    cmd(
        archiver,
        "--rsh", "ssh",
        "--remote-path", "borg",
        "benchmark",
        "crud",
        archiver.input_path
    )
