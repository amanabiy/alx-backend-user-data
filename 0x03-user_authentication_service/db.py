"""DB module
"""
from typing import TypeVar
from xml.etree.ElementPath import find
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
import bcrypt

from user import Base
from user import User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
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
        """ save the user to the database
        """
        session = self._session
        new_user = User(email=email, hashed_password=hashed_password)
        session.add(new_user)
        session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """ find the first user
        """
        session = self._session
        try:
            user = session.query(User).filter_by(**kwargs).first()
        except InvalidRequestError:
            raise (InvalidRequestError)
        if user is None:
            raise (NoResultFound)
        return user

    def update_user(self, user_id, **kwargs) -> None:
        """ update a given user by its Id
        """
        _id = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if not hasattr(_id, key):
                raise ValueError
            setattr(_id, key, value)
        self._session.commit()
