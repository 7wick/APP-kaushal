from flask import jsonify, make_response, abort
from flask_restful import reqparse, Resource
from services.UsersService import *

session_parser = reqparse.RequestParser()
session_parser.add_argument('email', type=str, default="", location='form')
session_parser.add_argument('password', type=str, default="", location='form')


class Session(Resource):

    def post(self):
        try:
            session_args = session_parser.parse_args()
            if len(session_args.email) == 0 or len(session_args.password) == 0:
                return make_response(jsonify(message="email and password are required"), 401)
            user_exists = find_user_by_email(session_args.email)
            if user_exists is not None and user_exists.password_hash == get_hash(session_args.password.encode('utf-8')):
                access_token = update_token(session_args.email)
                return make_response(jsonify({"message": "Session updated!", "Access Token": access_token,
                                              "status code": 200}), 200)
            else:
                return make_response(jsonify(message="Invalid credentials"), 401)
        except Exception as e:
            print(e)
            return make_response(jsonify(message="Incorrect URI or Internal error"), 500)
