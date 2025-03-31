class ConfidantError(Exception):
    """Base exception for Confidant-Py."""
    pass


# --- Credentials File Errors ---
class CredentialsFileNotFoundError(ConfidantError):
    """Raised when the credentials file is not found."""
    def __init__(self, filename="confidant-cred.json"):
        super().__init__(f"Credentials file '{filename}' not found. Please ensure it exists in the correct location.")


class InvalidCredentialsFormatError(ConfidantError):
    """Raised when the credentials file has an invalid format."""
    def __init__(self, message="Invalid credentials file format. Ensure it contains 'username' and 'private_key'."):
        super().__init__(message)


# --- API Errors ---
class APIServerUnavailableError(ConfidantError):
    """Raised when the API server is down or unreachable."""
    def __init__(self, message="Failed to connect to the API server. Ensure the server is running on localhost:8000."):
        super().__init__(message)


class APIRequestError(ConfidantError):
    """Raised when an API request fails with a non-200 status code."""
    def __init__(self, status_code, message=""):
        super().__init__(f"API request failed with status {status_code}. {message}")


class InvalidAPIResponseError(ConfidantError):
    """Raised when the API response is invalid or malformed."""
    def __init__(self, message="Invalid API response. Ensure the API is returning correctly formatted data."):
        super().__init__(message)


# --- Encryption & Decryption Errors ---
class PrivateKeyDecryptionError(ConfidantError):
    """Raised when decryption using the private key fails."""
    def __init__(self, message="Decryption failed. Ensure the correct private key is being used."):
        super().__init__(message)


class InvalidEncryptedDataError(ConfidantError):
    """Raised when the API response contains invalid or missing encryption fields."""
    def __init__(self, message="Received invalid encrypted data from API. Ensure the API response is correctly formatted."):
        super().__init__(message)


class EncryptionKeyNotFoundError(ConfidantError):
    """Raised when the required encryption key is missing."""
    def __init__(self, message="Encryption key not found. Ensure it is correctly set in the credentials file."):
        super().__init__(message)
