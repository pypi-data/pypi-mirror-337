import sys
import os
import pytest
from unittest.mock import patch, MagicMock
from PyQt6.QtWidgets import QApplication, QPushButton, QLabel
from src.ui import AntivirusUI
from src import main


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


@pytest.fixture(scope="module")
def app():
    """Fixture to create a QApplication instance."""
    app = QApplication([])
    return app


@pytest.fixture
def antivirus_ui(app):
    """Fixture to create an instance of AntivirusUI."""
    return AntivirusUI()


# ------------------- Tests for AntivirusUI -------------------

def test_ui_initialization(antivirus_ui):
    """Test that the AntivirusUI initializes correctly."""
    assert antivirus_ui.windowTitle() == "Antivirus Project"
    assert antivirus_ui.server_thread is None
    assert antivirus_ui.server_running is False


def test_create_main_screen(antivirus_ui):
    """Test that the main screen is created without errors."""
    antivirus_ui.create_main_screen()
    assert antivirus_ui.layout.count() > 0  # Ensure widgets are added to the layout


def test_scan_button(antivirus_ui):
    """Test that the Scan for Malware button is present and functional."""
    antivirus_ui.create_main_screen()
    scan_button = antivirus_ui.layout.itemAt(1).widget()
    assert isinstance(scan_button, QPushButton)
    assert scan_button.text() == "Scan for Malware"


def test_firewall_button(antivirus_ui):
    """Test that the Manage Firewall button is present and functional."""
    antivirus_ui.create_main_screen()
    firewall_button = antivirus_ui.layout.itemAt(2).widget()
    assert isinstance(firewall_button, QPushButton)
    assert firewall_button.text() == "Manage Firewall"


# ------------------- Tests for main.py -------------------

def test_is_ip_allowed():
    """Test the is_ip_allowed function."""
    assert main.is_ip_allowed("192.168.1.1") is True
    assert main.is_ip_allowed("203.0.113.1") is False
    assert main.is_ip_allowed("8.8.8.8") is False


def test_add_allowed_ip():
    """Test adding an allowed IP."""
    main.add_allowed_ip("8.8.8.8")
    assert "8.8.8.8" in main.get_firewall_rules()["allow"]


def test_add_blocked_ip():
    """Test adding a blocked IP."""
    main.add_blocked_ip("8.8.4.4")
    assert "8.8.4.4" in main.get_firewall_rules()["block"]


def test_get_firewall_rules():
    """Test retrieving firewall rules."""
    rules = main.get_firewall_rules()
    assert "allow" in rules
    assert "block" in rules


def test_rate_limiter():
    """Test the RateLimiter class."""
    limiter = main.RateLimiter(rate=5, per=1)
    assert limiter.allow_packet() is True
    assert limiter.allow_packet() is True
    assert limiter.allow_packet() is True
    assert limiter.allow_packet() is True
    assert limiter.allow_packet() is True
    assert limiter.allow_packet() is False  # Exceeds the rate limit


@patch("src.main.psutil.process_iter")
def test_scan_running_processes(mock_process_iter):
    """Test scanning running processes."""
    mock_process = MagicMock()
    mock_process.info = {"pid": 1234, "name": "malicious.exe", "exe": "path/to/malicious.exe"}
    mock_process_iter.return_value = [mock_process]

    with patch("builtins.open", MagicMock()) as mock_open:
        mock_open.return_value.read.return_value = b"malicious content"

        results = main.scan_running_processes()

    assert any("malicious.exe" in result for result in results), "Malicious process was not detected"


@patch("src.main.socket.socket")
def test_start_server(mock_socket):
    """Test starting the server."""
    mock_socket_instance = MagicMock()
    mock_socket.return_value = mock_socket_instance

    def mock_server_running_callback():
        return False

    def mock_server_socket_callback(server):
        pass

    main.start_server(mock_server_running_callback, mock_server_socket_callback)

    mock_socket.assert_called_once()
    mock_socket_instance.bind.assert_called_once_with(("0.0.0.0", 9999))
    mock_socket_instance.listen.assert_called_once()


@patch("src.main.socket.socket")
def test_handle_client(mock_socket):
    """Test handling a client connection."""
    # Mock a client socket
    mock_client_socket = MagicMock()
    mock_client_socket.recv.return_value = b"test data"

    # Mock the server socket's accept method
    mock_socket_instance = MagicMock()
    mock_socket_instance.accept.return_value = (mock_client_socket, ("192.168.1.1", 12345))

    # Mock the is_ip_allowed function to return True
    with patch("src.main.is_ip_allowed", return_value=True):
        main.handle_client(mock_client_socket, ("192.168.1.1", 12345))

    # Assert that recv was called
    mock_client_socket.recv.assert_called()

    # Assert that close was NOT called since the IP is allowed
    mock_client_socket.close.assert_not_called()