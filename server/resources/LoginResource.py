from http import HTTPStatus

from flask import request
from flask_jwt_extended import create_access_token
from passlib.hash import pbkdf2_sha256

from models import UserModel

from .api import BaseResource


class LoginResource(BaseResource):
    path = "/login"

    @classmethod
    def post(cls):
        args = request.get_json()

        required_args = {"username", "password"}
        
        if required_args - set(list(args.keys())):
            return {"error": f"{", ".join(list(required_args - args))} are required json fields"}, HTTPStatus.BAD_REQUEST

        username = args.get("username")
        password = args.get("password")

        try:
            user = UserModel.get_by_username(username)
            
            if pbkdf2_sha256.verify(password, user._password):
                token = create_access_token(user.id)
                return {
                    "message": "successfull login",
                    "user": user.json(),
                    "access_token": token
                }, HTTPStatus.OK
            else:
                return {"error": "invalid credentials"}, HTTPStatus.BAD_REQUEST

        except Exception as e:
            return {"error": str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR

