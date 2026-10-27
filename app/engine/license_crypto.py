import hashlib
from cryptography.fernet import Fernet
from pathlib import Path

class ADKLicenseVault:
    @staticmethod
    def generate_license_token(order_id: str, package_id: str, secret_salt: str) -> str:
        entropy = f"{order_id}:{package_id}:{secret_salt}".encode("utf-8")
        return hashlib.sha256(entropy).hexdigest()

    @staticmethod
    def encrypt_package(source_zip: Path, target_encrypted: Path) -> str:
        key = Fernet.generate_key()
        cipher = Fernet(key)
        with open(source_zip, "rb") as f_in:
            encrypted_data = cipher.encrypt(f_in.read())
        with open(target_encrypted, "wb") as f_out:
            f_out.write(encrypted_data)
        return key.decode("utf-8")
