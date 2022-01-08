#!/usr/bin/env python3
"""
Hash password
"""
from typing import ByteString
import bcrypt  # type: ignore


def hash_password(password: str) -> bytes:
    """
    returns the hashed byte string of a password
    """
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    checks if the password matches
    """
    if bcrypt.checkpw(password, hashed_password):
        return True
    else:
        return False
