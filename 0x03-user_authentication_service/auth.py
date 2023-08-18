#!/usr/bin/env python3
"""defines the password hash function
"""
import bcrypt
import uuid
from db import DB
from typing import Union
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _generate_uuid():
    """
    Generate a new UUID and return its string representation.
    This function is private to the auth module and should
    not be used outside of it.
    """
    new_uuid = uuid.uuid4()
    return str(new_uuid)


def _hash_password(password: str) -> bytes:
    """
    Hashes the input password using bcrypt.

    Args:
        password (str): The input password to be hashed.

    Returns:
        bytes: Salted hash of the input password.
    """
    if password and isinstance(password, str):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user.

        Args:
            email (str): The email of the user.
            password (str): The password of the user.

        Returns:
            User: The created User object.

        Raises:
            ValueError: If a user with the same email already exists.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists.")
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)

        return user

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validate user login.

        Args:
            email (str): The email of the user.
            password (str): The password of the user.

        Returns:
            bool: True if login is valid, False otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False

        hashed_password = user.hashed_password

        return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

    def create_session(self, email: str) -> str:
        """
        Create a session for the user and return the session ID.

        Args:
            email (str): The email of the user.

        Returns:
            str: The generated session ID.
        """
        try:
            user = self._db.find_user_by(email=email)

            session_id = _generate_uuid()
            user.session_id = session_id
            self._db._session.commit()

            return session_id
        except Exception:
            pass

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """
        Get the corresponding User based on the session ID.

        Args:
            session_id (str): The session ID to look up.

        Returns:
            User or None: The corresponding User object if found,
            otherwise None.
        """
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str):
        """
        Get the corresponding User based on the session ID.

        Args:
            session_id (str): The session ID to look up.

        Returns:
            User or None: The corresponding User object if found,
            otherwise None.
        """
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int):
        """
        Destroy the session of the corresponding user.

        Args:
            user_id (int): The user ID whose session needs to be destroyed.

        Returns:
            None
        """
        try:
            user = self._db.find_user_by(id=user_id)
            user.session_id = None
            self._db._session.commit()
        except NoResultFound:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """
        Get a reset password token for the user.

        Args:
            email (str): The email of the user.

        Returns:
            str: The generated reset password token.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError

        reset_token = str(uuid.uuid4())
        user.reset_token = reset_token
        self._db._session.commit()

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Update the user's password using a reset token.

        Args:
            reset_token (str): The reset token associated with the user.
            password (str): The new password to be set.

        Returns:
            None
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError

        hashed_password = _hash_password(password)
        user.hashed_password = hashed_password
        user.reset_token = None
        self._db._session.commit()

        return reset_token
