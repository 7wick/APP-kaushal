from random import randrange
from flask import make_response, jsonify
from flask_restful import reqparse, Resource
from services.LearnersService import *
import sys

post_parser = reqparse.RequestParser()
post_parser.add_argument('first_name', type=str, required=True, location='args')
post_parser.add_argument('last_name', type=str, required=True, location='args')
post_parser.add_argument('email', type=str, required=True, location='args')
post_parser.add_argument('password', type=str, required=True, location='args')
post_parser.add_argument('education', type=str, required=False, location='args')

patch_parser = reqparse.RequestParser()
patch_parser.add_argument('first_name', type=str, location='form')
patch_parser.add_argument('last_name', type=str, location='form')
patch_parser.add_argument('education', type=str, location='form')

get_learners_parser = reqparse.RequestParser()
get_learners_parser.add_argument('pagesize', type=int, location='args')
get_learners_parser.add_argument('page', type=int, location='args')

headers = {'Content-Type': 'application/json'}


class Learners(Resource):
    def get(self, pagesize=None, page=None):
        try:
            args = get_learners_parser.parse_args()
            learners = all_learners()
            if not all(value is None for value in args.values()):
                if args.page is None:
                    args.page = 1  # default page
                if args.pagesize is None:
                    args.pagesize = 5  # default pagesize
                start = (args.page - 1)*args.pagesize
                end = args.page*args.pagesize
                if start > end:
                    return make_response(jsonify(message="pagination values incorrect!"), 401)
                learners = learners[start:end]  # pagination
                if not len(learners):
                    return make_response(jsonify(message="No data for current pagination"), 404)
            return make_response(learners.to_json(), 200, headers)
        except Exception:
            return make_response(jsonify(message="Database Empty!"), 404)


class Learner(Resource):
    def get(self, learner_id=None):
        try:
            if find_learner_by_ID(learner_id) is not None:
                learner = find_learner_by_ID(learner_id)
                return make_response(learner.to_json(), 200, headers)
            else:
                return make_response(jsonify(message="Invalid learner ID"), 404)
        except Exception:
            return make_response(jsonify(message="Incorrect URI"), 401)

    def delete(self, learner_id=None):
        try:
            if find_learner_by_ID(learner_id):
                delete_learner_by_ID(learner_id)
                return make_response(jsonify(message="Record deleted successfully!"), 200)
            else:
                return make_response(jsonify(message="Invalid learner ID!"), 404)
        except Exception:
            return make_response(jsonify(message="Incorrect URI"), 401)

    def post(self):
        learner_id = sys.maxsize  # setting max integer as default learner_id
        try:
            args = post_parser.parse_args()
        except Exception:
            return make_response(jsonify(message="Missing parameters!"), 401)
        generated_flag = True
        while generated_flag:
            learner_id = randrange(1000, 9999)
            if find_learner_by_ID(learner_id) is None:
                generated_flag = False
        create_learner(learner_id, args.first_name, args.last_name, args.email, args.education)
        access_token = create_user(args.email, args.password)
        return make_response(jsonify({"message": "Record created successfully", "ID": learner_id,
                                      "Access Token": access_token, "status code": 200}), 200)

    def patch(self, learner_id):
        try:
            args = patch_parser.parse_args()
            if all(value is None for value in args.values()):  # checks if all args are None
                return make_response(jsonify(message="Nothing to update"), 200)
            if find_learner_by_ID(learner_id):
                learner = update_learner(learner_id, args.first_name, args.last_name, args.education)
                return make_response(learner.to_json(), 200, headers)
            else:
                return make_response(jsonify(message="Invalid learner ID"), 404)
        except Exception:
            return make_response(jsonify(message="Incorrect URI"), 401)
