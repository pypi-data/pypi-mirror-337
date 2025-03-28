import socket
from .config import load_config

def get_socket_path():
    return load_config().get("socket_path", "/tmp/sysmon.sock")

def send_command(message: str) -> str:
    try:
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
            client.connect(get_socket_path())
            client.sendall(message.encode())
            return client.recv(1024).decode()
    except FileNotFoundError:
        return "Daemon is not running (socket not found)"

def get_metrics():
    return send_command("metrics")

def get_status():
    return send_command("status")

def shutdown_daemon():
    return send_command("shutdown")

