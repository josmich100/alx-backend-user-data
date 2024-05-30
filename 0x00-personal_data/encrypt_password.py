#!/usr/bin/env python3
"""
Encrypting passwords with bcrypt.
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Checks if a password is valid.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
