#!/usr/bin/env python3
"""
Main module
"""


import requests


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
BASE_URL = "http://0.0.0.0:5000"


def register_user(email: str, password: str) -> None:
    """Register a user
    """
    response = requests.post(f"{BASE_URL}/users", data={"email": email,
                             "password": password})
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "user created"}
    response = requests.post(f"{BASE_URL}/users", data={"email": email,
                             "password": password})
    assert response.status_code == 400
    assert response.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    """Log in with wrong password
    """
    response = requests.post(f"{BASE_URL}/sessions", data={"email": email,
                             "password": password})
    assert response.status_code == 401
    assert response.json() == {"message": "wrong password"}


def log_in(email: str, password: str) -> str:
    """Log in
    """
    response = requests.post(f"{BASE_URL}/sessions", data={"email": email,
                             "password": password})
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "logged in"}
    return response.cookies.get("session_id")


def profile_unlogged() -> None:
    """Profile unlogged
    """
    response = requests.get(f"{BASE_URL}/profile")
    assert response.status_code == 403
    assert response.json() == {"message": "Unauthorized"}


def profile_logged(session_id: str) -> None:
    """Profile logged
    """
    response = requests.get(f"{BASE_URL}/profile",
                            cookies={"session_id": session_id})
    assert response.status_code == 200
    assert response.json() == {"email": EMAIL}


def log_out(session_id: str) -> None:
    """Log out
    """
    response = requests.delete(f"{BASE_URL}/sessions",
                               cookies={"session_id": session_id})
    assert response.status_code == 200
    assert response.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """Reset password token
    """
    response = requests.post(f"{BASE_URL}/reset_password",
                             data={"email": email})
    assert response.status_code == 200
    return response.json()["reset_token"]


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Update password
    """
    response = requests.put(f"{BASE_URL}/reset_password",
                            data={"email": email, "reset_token": reset_token,
                            "new_password": new_password})
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "password updated"}


if __name__ == "__main__":
    """Main"""
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
