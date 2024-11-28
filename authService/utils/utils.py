import hashlib


def get_hash_password(password: str):
    m = hashlib.sha512()
    m.update(password.encode('utf-8'))
    return m.hexdigest()