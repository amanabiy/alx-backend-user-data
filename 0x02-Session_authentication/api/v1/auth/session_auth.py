#!/usr/bin/env python3
"""
A session athentication module
"""
from uuid import uuid4
from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    """ session authentication
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ create session """
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        sessionId = uuid4()
        self.user_id_by_session_id[sessionId] = user_id
        return sessionId

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ user_id """
        if session_id is None:
            return None
        if isinstance(session_id, str):
            return None
        return SessionAuth.user_id_by_session_id.get(session_id, None)

    def current_user(self, request=None) -> str:
        """ return the current user
        """
        if request is None:
            return None
        cookie = self.session_cookie(request)
        if cookie is None:
            return None
        user_id = self.user_id_for_session_id(cookie)
        return User.get(user_id)
        
