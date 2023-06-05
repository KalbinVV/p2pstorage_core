import hashlib
from enum import IntEnum


class CryptMode(IntEnum):
    UNENCRYPTED = 1
    RSA = 2


def get_hash_of_file(file_path: str) -> str:
    buf_size = 65536  # 64kb chunks

    sha256 = hashlib.sha3_256()

    with open(file_path, 'rb') as f:
        while True:
            data = f.read(buf_size)

            if not data:
                break

            sha256.update(data)

    return sha256.hexdigest()
