#!/usr/bin/env python3
""" Authentication module
"""
from uuid import uuid4
from sqlalchemy.orm.exc import NoResultFound
from typing import TypeVar
import bcrypt


from db import DB


def _hash_password(password: str) -> bytes:
    """ hashes password
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)


def _generate_uuid() -> str:
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> TypeVar('User'):
        """ Registers users
        """
        try:
            find_user = self._db.find_user_by(email=email)
            raise ValueError(f'User {email} already exists')
        except NoResultFound:
            hashed_pwd = _hash_password(password)
            return self._db.add_user(email, hashed_pwd)

    def valid_login(self, email: str, password: str) -> bool:
        """ validate login credentials
        """
        try:
            find_user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode("utf8"),
                              find_user.hashed_password):
                return True
            else:
                raise ValueError
        except Exception:
            return False

    def create_session(self, email: str) -> str:
        """ Create session and save to the user
        """
        try:
            user = self._db.find_user_by(email=email)
            user_session = _generate_uuid()
            self._db.update_user(user.id, session_id=user_session)
            return user_session
        except Exception:
            return

    def get_user_from_session_id(self, session_id: str) -> TypeVar('User'):
        """ Get the user form session id
        """
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except Exception:
            return None

    def destroy_session(self, user_id: int) -> None:
        """ Destroys a session
        """
        try:
            user = self._db.update_user(user_id, session_id=None)
            return None
        except Exception:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """ generate a UUID and update the user’s reset_token
        """
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except Exception:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """ Updates the password if reset_token exists
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            pwd = _hash_password(password)
            self._db.update_user(user.id, hashed_password=pwd, reset_token=None)
        except NoResultFound:
            raise ValueError
