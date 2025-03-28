import pytest
from unittest.mock import patch, MagicMock
from sysmon_sdk import core

# Mock socket communication for send_command
@patch("sysmon_sdk.core.socket.socket")
def test_send_command(mock_socket_class):
    mock_socket = MagicMock()
    mock_socket.recv.return_value = b"Processed: test"
    mock_socket_class.return_value.__enter__.return_value = mock_socket

    response = core.send_command("test")
    assert response == "Processed: test"
    mock_socket.connect.assert_called_once()
    mock_socket.sendall.assert_called_with(b"test")

def test_get_status():
    with patch("sysmon_sdk.core.send_command") as mock_send:
        mock_send.return_value = "Processed: status"
        result = core.get_status()
        assert result == "Processed: status"

def test_get_metrics():
    with patch("sysmon_sdk.core.send_command") as mock_send:
        mock_send.return_value = "Processed: metrics"
        result = core.get_metrics()
        assert result == "Processed: metrics"

def test_shutdown_daemon():
    with patch("sysmon_sdk.core.send_command") as mock_send:
        mock_send.return_value = "Processed: shutdown"
        result = core.shutdown_daemon()
        assert result == "Processed: shutdown"

