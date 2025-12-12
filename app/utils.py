from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher

pwd_context = PasswordHash(hashers=[Argon2Hasher()])

def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)