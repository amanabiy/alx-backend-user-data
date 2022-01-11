#!/usr/bin/env python3
""" Basic Authentication Module
"""
import base64
from typing import TypeVar
from api.v1.auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    """ Basic Authentication Class
    """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ Extracts the username and password
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if authorization_header[0:6] != "Basic ":
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """ Decode bas464
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            auth = base64.b64decode(base64_authorization_header)
            return auth.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """ Extract username and password
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ":" not in decoded_base64_authorization_header:
            return (None, None)
        username, password = decoded_base64_authorization_header.split(":")
        return (username, password)

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """ Returns the user instance
        Baed on Email and password
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            found = User.search({"email": user_email})
        except Exception:
            return None
        for user in found:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ retrieves the User instance for a request
        """
        authHeader = self.authorization_header(request)
        extracted_base64 = self.extract_base64_authorization_header(authHeader)
        decoded_auth = self.decode_base64_authorization_header(
            extracted_base64)
        username, password = self.extract_user_credentials(decoded_auth)
        return self.user_object_from_credentials(username, password)
