#!/usr/bin/env python3
"""
"""
import requests

BASE_URL = "http://172.23.86.6:5000"


def register_user(email: str, password: str) -> None:
    response = requests.post(
        f"{BASE_URL}/users", data={"email": email, "password": password})
    assert response.status_code == 200, "Failed to register user"


def log_in_wrong_password(email: str, password: str) -> None:
    response = requests.post(
        f"{BASE_URL}/sessions", data={"email": email, "password": password})
    assert response.status_code == 401, "Login with wrong password should fail"


def log_in(email: str, password: str) -> str:
    response = requests.post(
        f"{BASE_URL}/sessions", data={"email": email, "password": password})
    assert response.status_code == 200, f"Failed to log in"
    return response.cookies.get("session_id")


def profile_unlogged() -> None:
    response = requests.get(f"{BASE_URL}/profile")
    assert response.status_code == 403, \
        "Profile request should be forbidden when unlogged"


def profile_logged(session_id: str) -> None:
    response = requests.get(
        f"{BASE_URL}/profile", cookies={"session_id": session_id})
    assert response.status_code == 200, \
        f"Failed to retrieve profile when logged in"


def log_out(session_id: str) -> None:
    response = requests.delete(
        f"{BASE_URL}/sessions", cookies={"session_id": session_id})
    assert response.status_code == 200, f"Failed to log out"


def reset_password_token(email: str) -> str:
    response = requests.post(
        f"{BASE_URL}/reset_password", data={"email": email})
    assert response.status_code == 200, "Failed to get reset password token"
    return response.json()["reset_token"]


def update_password(email: str, reset_token: str, new_password: str) -> None:
    response = requests.put(
        f"{BASE_URL}/reset_password",
        data={
            "email": email,
            "reset_token": reset_token,
            "new_password": new_password
        }
    )
    assert response.status_code == 200, f"Failed to update password"


if __name__ == "__main__":
    EMAIL = "guillaume@holberton.io"
    PASSWD = "b4l0u"
    NEW_PASSWD = "t4rt1fl3tt3"

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
