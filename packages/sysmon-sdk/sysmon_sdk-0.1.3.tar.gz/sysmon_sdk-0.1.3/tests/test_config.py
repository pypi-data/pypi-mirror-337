from sysmon_sdk import config
import os
import json

def test_env_var_overrides_config(monkeypatch):
    monkeypatch.setenv("SYSMON_SOCKET_PATH", "/tmp/from_env.sock")

    cfg = config.load_config()

    assert cfg["socket_path"] == "/tmp/from_env.sock"

def test_fallback_to_config_json(monkeypatch):
    monkeypatch.delenv("SYSMON_SOCKET_PATH", raising=False)
    cfg = config.load_config()
    assert cfg["socket_path"] == "/tmp/sysmon.sock"


import shutil

def test_fallback_to_default_when_config_missing(monkeypatch):
    monkeypatch.delenv("SYSMON_SOCKET_PATH", raising=False)

    # Temporarily move config.json out of the way
    original = "sysmon_sdk/config.json"
    backup = "sysmon_sdk/config.json.bak"
    shutil.move(original, backup)

    try:
        cfg = config.load_config()
        assert cfg["socket_path"] == "/tmp/sysmon.sock"  # hardcoded default
    finally:
        shutil.move(backup, original)  # restore config.json



def test_fallback_to_user_config(monkeypatch, tmp_path):
    monkeypatch.delenv("SYSMON_SOCKET_PATH", raising=False)

    # Temporarily rename local config.json
    local_config = "sysmon_sdk/config.json"
    backup = "sysmon_sdk/config.json.bak"
    if os.path.exists(local_config):
        os.rename(local_config, backup)

    # Create ~/.sysmon/config.json with test data
    user_config_dir = os.path.expanduser("~/.sysmon")
    os.makedirs(user_config_dir, exist_ok=True)
    user_config_file = os.path.join(user_config_dir, "config.json")

    test_path = "/tmp/from_user_config.sock"
    with open(user_config_file, "w") as f:
        json.dump({"socket_path": test_path}, f)

    try:
        from sysmon_sdk.config import load_config
        cfg = load_config()
        assert cfg["socket_path"] == test_path
    finally:
        os.remove(user_config_file)
        if os.path.exists(backup):
            os.rename(backup, local_config)

