#!/usr/bin/env python3
"""
A session athentication module
"""
from uuid import uuid4
from api.v1.auth.auth import Auth


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
