import json
import hashlib
import requests
from pathlib import Path
from requests.exceptions import ConnectionError as ReqConnectionError, RequestException
from .decryption import decrypt_envs
from .exceptions import (
    CredentialsFileNotFoundError,
    InvalidCredentialsFormatError,
    APIRequestError,
    APIServerUnavailableError,
    InvalidEncryptedDataError
)

DEFAULT_CREDENTIALS_FILE = "confidant-cred.json"
API_URL = "http://localhost:8000/api/get-sdk-keys/"

class ConfidantLoader:
    def __init__(self, credentials_file=DEFAULT_CREDENTIALS_FILE):
        self.credentials_file = credentials_file
        self.username, self.public_key, self.private_key = self.load_credentials()

    def load_credentials(self):
        """Loads credentials from the JSON file."""
        credentials_path = Path(self.credentials_file)

        if not credentials_path.exists():
            raise CredentialsFileNotFoundError(self.credentials_file)

        try:
            with open(credentials_path, "r") as file:
                credentials = json.load(file)
        except json.JSONDecodeError:
            raise InvalidCredentialsFormatError()

        if "username" not in credentials or "public_key" not in credentials or "private_key" not in credentials:
            raise InvalidCredentialsFormatError()

        return credentials["username"], credentials["public_key"], credentials["private_key"]

    def compute_public_key_hash(self):
        """Computes the SHA-256 hash of the stored public key."""
        return hashlib.sha256(self.public_key.encode()).hexdigest()

    def fetch_encrypted_envs(self):
        """Fetches encrypted environment variables from the API with username and public key hash in headers."""
        headers = {
            "X-Username": self.username,  # Send username in headers
            "X-Public-Key-Hash": self.compute_public_key_hash(),  # Send SHA-256 hash of the public key
            "Content-Type": "application/json"
        }

        payload = {
            "username": self.username  # Send username in JSON body
        }

        try:
            response = requests.post(API_URL, headers=headers, json=payload)
        except ReqConnectionError:
            raise APIServerUnavailableError()
        except RequestException as e:
            raise APIRequestError("Unknown", str(e))

        if response.status_code != 200:
            raise APIRequestError(response.status_code, response.text)

        try:
            data = response.json()
        except json.JSONDecodeError:
            raise InvalidEncryptedDataError("Invalid JSON response from API.")

        return data

    def get_envs(self):
        """Fetches and decrypts environment variables."""
        encrypted_data = self.fetch_encrypted_envs()

        return decrypt_envs(
            encrypted_envs_b64=encrypted_data.get("encrypted_data"),
            encrypted_aes_key_b64=encrypted_data.get("encrypted_aes_key"),
            iv_b64=encrypted_data.get("iv"),
            private_key_pem=self.private_key
        )
