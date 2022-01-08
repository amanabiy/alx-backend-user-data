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
