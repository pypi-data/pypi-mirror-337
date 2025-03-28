import subprocess
import pytest

def run_cli(command):
    result = subprocess.run(
        ["coverage", "run", "--parallel-mode", "-m", "sysmon_sdk.cli", command],
        capture_output=True,
        text=True
    )
    return result.stdout.strip()

def test_status():
    output = run_cli("status")
    assert "Processed" in output

def test_metrics():
    output = run_cli("metrics")
    assert "Processed" in output

def test_invalid():
    output = run_cli("help")
    assert "Invalid command" in output

@pytest.mark.order("last")
def test_shutdown():
    output = run_cli("shutdown")
    assert "Processed" in output or "Daemon is not running" in output



