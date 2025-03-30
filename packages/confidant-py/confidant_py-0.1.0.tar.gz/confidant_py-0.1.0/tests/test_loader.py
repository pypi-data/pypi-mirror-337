import pytest
import json
import requests
from unittest.mock import patch, mock_open
from confidant_py.loader import ConfidantLoader
from confidant_py.exceptions import (
    CredentialsFileNotFoundError,
    InvalidCredentialsFormatError,
    APIRequestError,
    APIServerUnavailableError,
    InvalidEncryptedDataError,
)
    
MOCK_CREDENTIALS = {
    "username": "ghn8",
    "private_key": "mock_private_key"
}

MOCK_ENCRYPTED_RESPONSE = {
    "encrypted_data": "mock_encrypted_data",
    "encrypted_aes_key": "mock_encrypted_aes_key",
    "iv": "mock_iv"
}

def mock_requests_post(*args, **kwargs):
    """Simulates a successful API response"""
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code
        
        def json(self):
            return self.json_data

    return MockResponse(MOCK_ENCRYPTED_RESPONSE, 200)


@pytest.fixture
def mock_credentials_file():
    """Mocks opening a credentials file"""
    credentials_json = json.dumps(MOCK_CREDENTIALS)
    with patch("builtins.open", mock_open(read_data=credentials_json)):
        yield


@pytest.fixture
def mock_requests():
    """Mocks requests.post"""
    with patch("requests.post", side_effect=mock_requests_post):
        yield


def test_loader_initialization(mock_credentials_file):
    """Test initialization of ConfidantLoader with valid credentials file"""
    loader = ConfidantLoader()
    assert loader.username == "ghn8"
    assert loader.private_key == "mock_private_key"


def test_loader_credentials_file_missing():
    """Test behavior when credentials file is missing"""
    with patch("pathlib.Path.exists", return_value=False):
        with pytest.raises(CredentialsFileNotFoundError):
            ConfidantLoader()


def test_loader_invalid_credentials_format():
    """Test behavior when credentials file contains invalid JSON"""
    with patch("builtins.open", mock_open(read_data="invalid_json")):
        with pytest.raises(InvalidCredentialsFormatError):
            ConfidantLoader()


def test_loader_missing_username_field():
    """Test behavior when credentials file lacks username field"""
    invalid_credentials = json.dumps({"private_key": "mock_private_key"})
    with patch("builtins.open", mock_open(read_data=invalid_credentials)):
        with pytest.raises(InvalidCredentialsFormatError):
            ConfidantLoader()


def test_loader_missing_private_key():
    """Test behavior when credentials file lacks private_key field"""
    invalid_credentials = json.dumps({"username": "ghn8"})
    with patch("builtins.open", mock_open(read_data=invalid_credentials)):
        with pytest.raises(InvalidCredentialsFormatError):
            ConfidantLoader()


def test_fetch_encrypted_envs_success(mock_credentials_file, mock_requests):
    """Test successful retrieval of encrypted environment variables"""
    loader = ConfidantLoader()
    data = loader.fetch_encrypted_envs()
    assert data == MOCK_ENCRYPTED_RESPONSE


def test_fetch_encrypted_envs_server_unavailable(mock_credentials_file):
    """Test API failure due to server being unavailable"""
    with patch("requests.post", side_effect=requests.exceptions.ConnectionError):
        loader = ConfidantLoader()
        with pytest.raises(APIServerUnavailableError):
            loader.fetch_encrypted_envs()


def test_fetch_encrypted_envs_api_error(mock_credentials_file):
    """Test API failure with non-200 response"""
    def mock_failed_post(*args, **kwargs):
        class MockResponse:
            def __init__(self):
                self.status_code = 500
                self.text = "Internal Server Error"
            def json(self):
                return {"error": "Server error"}

        return MockResponse()

    with patch("requests.post", side_effect=mock_failed_post):
        loader = ConfidantLoader()
        with pytest.raises(APIRequestError, match="500"):
            loader.fetch_encrypted_envs()


def test_fetch_encrypted_envs_invalid_json(mock_credentials_file):
    """Test API failure due to invalid JSON response"""

    class MockResponse:
        def __init__(self):
            self.status_code = 200
            self.text = "Invalid JSON"

        def json(self):
            raise json.JSONDecodeError("Expecting value", self.text, 0)

    with patch("requests.post", return_value=MockResponse()):
        loader = ConfidantLoader()
        with pytest.raises(InvalidEncryptedDataError):
            loader.fetch_encrypted_envs()