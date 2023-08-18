#!/usr/bin/env python3
"""defines the password hash function
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _generate_uuid():
    """
    Generate a new UUID and return its string representation.
    This function is private to the auth module and should not be used outside of it.
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
        entered_password = password.encode('utf-8')
        print(f'==================== {entered_password} ================================')
        print(f'==================== {user.hashed_password} ================================')
        print(f'==================== {_hash_password(password)} ================================')

        return bcrypt.checkpw(password.encode('utf-8'), hashed_password)