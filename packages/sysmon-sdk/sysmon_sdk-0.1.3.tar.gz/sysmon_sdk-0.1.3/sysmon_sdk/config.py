import os
import json

DEFAULT_SOCKET_PATH = "/tmp/sysmon.sock"
DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")
USER_CONFIG_PATH = os.path.expanduser("~/.sysmon/config.json")

def load_config():
    env_path = os.environ.get("SYSMON_SOCKET_PATH")
    if env_path:
        print("Loaded socket path from SYSMON_SOCKET_PATH")
        return {"socket_path": env_path}

    if os.path.exists(DEFAULT_CONFIG_PATH):
        try:
            with open(DEFAULT_CONFIG_PATH) as f:
                print(f"Loaded socket path from {DEFAULT_CONFIG_PATH}")
                return json.load(f)
        except Exception:
            pass

    if os.path.exists(USER_CONFIG_PATH):
        try:
            with open(USER_CONFIG_PATH) as f:
                print(f"Loaded socket path from {USER_CONFIG_PATH}")
                return json.load(f)
        except Exception:
            pass

    print("Using built-in default socket path")
    return {"socket_path": DEFAULT_SOCKET_PATH}
