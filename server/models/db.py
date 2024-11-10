from __future__ import annotations

from typing import Dict, Any

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.extension import _FSAModel

from sqlalchemy.orm.attributes import InstrumentedAttribute


db = SQLAlchemy()


def init_app(app: Flask):
    global db

    db.init_app(app)
    with app.app_context():
        db.create_all()


class BaseModel(db.Model):
    __abstract__ = True

    def json(self) -> Dict[str, Any]:
        json_dict: Dict[str, Any] = dict()

        for field in self.__class__.__dict__.keys():
            if not field.startswith("_"):
                value = self.__class__.__dict__.get(field)
                if isinstance(value, InstrumentedAttribute):
                    json_dict[field] = self.__dict__.get(field)

        for property_field in self.__dir__():
            if not property_field.startswith("_"):
                if type(self.__class__.__dict__.get(property_field)) is property:
                    json_dict[property_field] = getattr(self, property_field)

        return json_dict

    def __str__(self) -> str:
        return str(self.json())

    @classmethod
    def get_by_id(cls, _id: int) -> BaseModel | None:
        return cls.query.get(_id)

    def save(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()
