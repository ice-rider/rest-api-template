from http import HTTPStatus

from flask import request
from flask_jwt_extended import create_access_token
from passlib.hash import pbkdf2_sha256

from models import UserModel

from .api import BaseResource


class RegisterResource(BaseResource):
    path = "/register"

    @classmethod
    def post(cls):
        args = request.get_json()

        required_args = {"firstname", "password", "username", "email"}
        
        if required_args - set(list(args.keys())):
            return {"error": f"{", ".join(list(required_args - args))} are required json fields"}, HTTPStatus.BAD_REQUEST

        firstname = args.get("firstname")
        lastname = args.get("lastname")
        username = args.get("username")
        password = args.get("password")
        email = args.get("email")

        if UserModel.get_by_email(email):
            return {"error": "user with this email already registered"}, HTTPStatus.CONFLICT

        if UserModel.get_by_username(username):
            return {"error": "user with this username already registered"}, HTTPStatus.CONFLICT

        try:
            password = pbkdf2_sha256.hash(password)

            user = UserModel(
                firstname = firstname,
                lastname = lastname,
                username = username,
                password = password,
                email = email
            )
            user.save()
            token = create_access_token(user.id)

            return {
                "message": "successfull registration",
                "user": user.json(),
                "access_token": token
            }, HTTPStatus.CREATED

        except Exception as e:
            return {"error": str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR

