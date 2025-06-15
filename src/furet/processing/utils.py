import hashlib


def getFileHash(path: str):
    with open(path, "rb") as file:
        digest = hashlib.file_digest(file, "sha256")
    return digest.hexdigest()