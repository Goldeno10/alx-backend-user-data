#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from typing import Dict

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a new user to the database.

        Args:
            email (str): User's email address.
            hashed_password (str): Hashed password.

        Returns:
            User: Created User object.
        """
        new_user = User()
        new_user.email = email
        new_user.hashed_password = hashed_password

        self._session.add(new_user)
        self._session.commit()

        return new_user

    def find_user_by(self, **kwargs: Dict) -> User:
        """
        Finds a user
        """
        valid_keys = ['id', 'email', 'session_id', 'reset_token']
        invalid_keys = set(kwargs.keys()) - set(valid_keys)

        if invalid_keys:
            raise InvalidRequestError

        query = self._session.query(User)

        for key, value in kwargs.items():
            if key == 'id':
                query = query.filter(User.id == value)
            elif key == 'email':
                query = query.filter(User.email == value)
            elif key == 'session_id':
                query = query.filter(User.session_id == value)
            elif key == 'reset_token':
                query = query.filter(User.reset_token == value)
        try:
            user = query.one()
        except Exception:
            raise NoResultFound
        return user

    def update_user(self, user_id: int, **kwargs: Dict) -> None:
        """
        Update a user's attributes in the database.

        Args:
            user_id (int): ID of the user to be updated.
            kwargs: Arbitrary keyword arguments representing
            attributes to update.

        Raises:
            InvalidRequestError: If invalid keys are provided in kwargs.
            NoResultFound: If no user is found with the given user_id.
            ValueError: If an argument that does not correspond to
            a user attribute is passed.
        """
        if not user_id or not isinstance(user_id, int):
            return

        valid_keys = ['email', 'hashed_password', 'session_id', 'reset_token']

        invalid_keys = set(kwargs.keys()) - set(valid_keys)
        if invalid_keys:
            raise ValueError

        try:
            user = self.find_user_by(id=user_id)
        except NoResultFound:
            raise NoResultFound

        for key, value in kwargs.items():
            setattr(user, key, value)

        self._session.commit()
