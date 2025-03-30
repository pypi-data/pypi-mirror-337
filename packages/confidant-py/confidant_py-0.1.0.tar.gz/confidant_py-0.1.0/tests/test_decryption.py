import pytest
import base64
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from confidant_py.decryption import decrypt_envs
from confidant_py.exceptions import (
    PrivateKeyDecryptionError,
    InvalidEncryptedDataError
)

# Generate a test RSA key pair
TEST_PRIVATE_KEY = rsa.generate_private_key(public_exponent=65537, key_size=2048)
TEST_PUBLIC_KEY = TEST_PRIVATE_KEY.public_key()

PRIVATE_KEY_PEM = base64.b64encode(
    TEST_PRIVATE_KEY.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
).decode()


def test_decrypt_envs_success():
    """Test successful decryption with valid encrypted data"""
    # Encrypt a sample AES key using the public key
    AES_KEY = b"1234567890abcdef"  # 16-byte AES key
    encrypted_aes_key = base64.b64encode(
        TEST_PUBLIC_KEY.encrypt(
            AES_KEY,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    ).decode()

    # Encrypt JSON data with AES
    sample_data = b'{"DB_URL": "mysql://localhost"}'
    iv = b"1234567890abcdef"  # 16-byte IV
    cipher = Cipher(algorithms.AES(AES_KEY), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padded_data = sample_data + bytes([16 - len(sample_data) % 16] * (16 - len(sample_data) % 16))
    encrypted_data = base64.b64encode(encryptor.update(padded_data) + encryptor.finalize()).decode()

    decrypted = decrypt_envs(
        encrypted_envs_b64=encrypted_data,
        encrypted_aes_key_b64=encrypted_aes_key,
        iv_b64=base64.b64encode(iv).decode(),
        private_key_pem=PRIVATE_KEY_PEM
    )

    assert decrypted == {"DB_URL": "mysql://localhost"}


def test_decrypt_envs_invalid_private_key():
    """Test decryption failure due to an incorrect private key"""
    with pytest.raises(PrivateKeyDecryptionError):
        decrypt_envs("mock_data", "mock_aes_key", "mock_iv", "invalid_key")


def test_decrypt_envs_invalid_encrypted_data():
    """Test decryption failure due to corrupted encrypted data"""
    with pytest.raises(PrivateKeyDecryptionError):
        decrypt_envs("invalid_data", "mock_aes_key", "mock_iv", PRIVATE_KEY_PEM)


def test_decrypt_envs_invalid_json():
    """Test failure when decrypted data is not valid JSON"""
    AES_KEY = b"1234567890abcdef"
    iv = b"1234567890abcdef"

    # Encrypt invalid JSON data
    invalid_json_data = b"invalid_json"
    cipher = Cipher(algorithms.AES(AES_KEY), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padded_invalid_json = invalid_json_data + bytes([16 - len(invalid_json_data) % 16] * (16 - len(invalid_json_data) % 16))
    encrypted_invalid_json = base64.b64encode(encryptor.update(padded_invalid_json) + encryptor.finalize()).decode()

    encrypted_aes_key = base64.b64encode(
        TEST_PUBLIC_KEY.encrypt(
            AES_KEY,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    ).decode()

    with pytest.raises(InvalidEncryptedDataError):
        decrypt_envs(encrypted_invalid_json, encrypted_aes_key, base64.b64encode(iv).decode(), PRIVATE_KEY_PEM)
