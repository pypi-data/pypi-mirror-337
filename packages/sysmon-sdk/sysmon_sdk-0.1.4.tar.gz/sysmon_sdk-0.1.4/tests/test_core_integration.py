from sysmon_sdk.core import get_status, get_metrics, shutdown_daemon

def test_get_status_real():
    result = get_status()
    assert result.startswith("Processed:")

def test_get_metrics_real():
    result = get_metrics()
    assert result.startswith("Processed:")

def test_shutdown_real():
    result = shutdown_daemon()
    assert result.startswith("Processed:")

