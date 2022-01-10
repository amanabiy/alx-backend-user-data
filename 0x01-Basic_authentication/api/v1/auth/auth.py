#!/usr/bin/env python3
""" Authentication Module
"""
from typing import List, TypeVar
from flask import request


class Auth:
    """ Authetication class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ path require authentication
        """
        if not path:
            return True
        if not excluded_paths or len(excluded_paths) == 0:
            return True
        if path[-1] != '/':
            path += '/'
        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """ Autherization header
        """
        if not request:
            return None
        return request.headers.get("Authorization", None)

    def current_user(self, request=None) -> TypeVar('User'):
        """ Current User
        """
        return None
