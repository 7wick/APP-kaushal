from random import randrange
from flask import make_response, jsonify
from flask_restful import reqparse, Resource
from services.LearnersService import *
import sys

get_parser = reqparse.RequestParser()
get_parser.add_argument('pagesize', type=int, location='args')
get_parser.add_argument('page', type=int, location='args')

headers = {'Content-Type': 'application/json'}


class Users(Resource):
    def get(self, pagesize=None, page=None):
        try:
            args = get_parser.parse_args()
            users = all_users()
            if not all(value is None for value in args.values()):
                if args.page is None:
                    args.page = 1  # default page
                if args.pagesize is None:
                    args.pagesize = 5  # default pagesize
                start = (args.page - 1)*args.pagesize
                end = args.page*args.pagesize
                if start > end:
                    return make_response(jsonify(message="pagination values incorrect!"), 401)
                users = users[start:end]  # pagination
                if not len(users):
                    return make_response(jsonify(message="No data for current pagination"), 404)
            return make_response(users.to_json(), 200, headers)
        except Exception:
            return make_response(jsonify(message="Database Empty!"), 404)


class User(Resource):
    def get(self, user_email=None):
        try:
            if find_user_by_email(user_email) is not None:
                user = find_user_by_email(user_email)
                return make_response(user.to_json(), 200, headers)
            else:
                return make_response(jsonify(message="Invalid user ID"), 404)
        except:
            return make_response(jsonify(message="Incorrect URI"), 401)

    # def patch(self, user_email):
    #     try:
    #         args = patch_parser.parse_args()
    #         if all(value is None for value in args.values()):  # checks if all args are None
    #             return make_response(jsonify(message="Nothing to update"), 200)
    #         if find_learner_by_ID(learner_id):
    #             learner = update_learner(learner_id, args.first_name, args.last_name, args.education)
    #             return make_response(learner.to_json(), 200, headers)
    #         else:
    #             return make_response(jsonify(message="Invalid learner ID"), 404)
    #     except Exception:
    #         return make_response(jsonify(message="Incorrect URI"), 401)
