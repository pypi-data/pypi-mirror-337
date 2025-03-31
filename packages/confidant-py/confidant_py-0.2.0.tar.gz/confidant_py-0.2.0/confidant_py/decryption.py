import base64
import json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from .exceptions import PrivateKeyDecryptionError, InvalidEncryptedDataError


def decrypt_envs(encrypted_envs_b64, encrypted_aes_key_b64, iv_b64, private_key_pem):
    """
    Decrypts environment variables using RSA (for AES key) and AES (for envs).
    """

    try:
        # Load the private key
        private_key = serialization.load_pem_private_key(
            base64.b64decode(private_key_pem.encode()), password=None
        )
    except Exception:
        raise PrivateKeyDecryptionError("Failed to load private key. Ensure it's in correct PEM format.")

    # Decrypt AES key using RSA private key
    try:
        aes_key = private_key.decrypt(
            base64.b64decode(encrypted_aes_key_b64),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    except Exception:
        raise PrivateKeyDecryptionError("Failed to decrypt AES key. Ensure the correct private key is used.")

    # Perform AES decryption
    try:
        cipher = Cipher(algorithms.AES(aes_key), modes.CBC(base64.b64decode(iv_b64)), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_data = decryptor.update(base64.b64decode(encrypted_envs_b64)) + decryptor.finalize()

        # Validate padding before removing
        padding_length = decrypted_data[-1]
        if padding_length > 16:  # AES block size is 16, padding should not exceed it
            raise PrivateKeyDecryptionError("Invalid padding in decrypted data.")

        decrypted_data = decrypted_data[:-padding_length]
    except Exception:
        raise PrivateKeyDecryptionError("AES decryption failed. Data might be corrupted.")

    # Convert decrypted data to JSON
    try:
        return json.loads(decrypted_data.decode())
    except json.JSONDecodeError:
        raise InvalidEncryptedDataError("Decrypted data is not valid JSON.")
