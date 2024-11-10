from __future__ import annotations

from .db import db, BaseModel


class UserModel(BaseModel):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String)
    lastname = db.Column(db.String, nullable=True)
    username = db.Column(db.String, unique=True)
    _password = db.Column(db.String(87))
    _email = db.Column(db.String, unique=True)

    def __init__(self, firstname: str, username: str, password: str, email: str, lastname: str = None):
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self._password = password
        self._email = email

    @classmethod
    def get_by_email(cls, email: str) -> UserModel | None:
        return cls.query.filter_by(_email=email).first()

    @classmethod
    def get_by_username(cls, _username: str) -> UserModel | None:
        return cls.query.filter_by(username=_username).first()
