"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from typing import TypeVar
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
    def _session(self):
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ save the user to the database
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """ find the first user
        """
        if not kwargs:
            raise InvalidRequestError
        # session = self._session
        try:
            user = self._session.query(User).filter_by(**kwargs).first()
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
