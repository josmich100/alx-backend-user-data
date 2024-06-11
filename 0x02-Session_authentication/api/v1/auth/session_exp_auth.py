#!/usr/bin/env python3
"""
SessionExpAuth class
"""


from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
from os import getenv


class SessionExpAuth(SessionAuth):
    """ SessionExpAuth class
    """
    session_duration = 0

    def __init__(self):
        """ __init__ method
        """
        try:
            self.session_duration = int(getenv("SESSION_DURATION"))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """ create_session method
        """
        try:
            session_id = super().create_session(user_id)
        except Exception:
            return None
        if session_id is None:
            return None
        self.user_id_by_session_id[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ user_id_for_session_id method
        """
        if session_id is None:
            return None
        try:
            session_dict = self.user_id_by_session_id.get(session_id)
        except Exception:
            return None
        if session_dict is None:
            return None
        if self.session_duration <= 0:
            return session_dict.get("user_id")
        if session_dict.get("created_at") is None:
            return None
        if (session_dict.get("created_at") +
                timedelta(seconds=self.session_duration) < datetime.now()):
            self.destroy_session(None)
            return None
        return session_dict.get("user_id")
