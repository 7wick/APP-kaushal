from flask import make_response, jsonify, request
from flask_jwt_extended import jwt_required
from flask_restful import reqparse, Resource
from services.LearnersService import *
from services.UsersService import generate_id

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
                start = (args.page - 1) * args.pagesize
                end = args.page * args.pagesize
                if start > end:
                    return make_response(jsonify(message="pagination values incorrect!"), 401)
                learners = learners[start:end]  # pagination
                if not len(learners):
                    return make_response(jsonify(message="No data for current pagination"), 404)
            return make_response(learners.to_json(), 200, headers)
        except Exception as e:
            print(e)
            return make_response(jsonify(message="Database Empty!"), 404)


class Learner(Resource):
    @jwt_required()
    def get(self, learner_id=None):
        try:
            learner = find_learner_by_ID(learner_id)
            token = request.headers.get('Authorization').split()[1]  # Get Bearer Token
            if learner is None:
                return make_response(jsonify(message="Invalid learner ID"), 404)
            elif token != find_user_by_ID(learner_id).access_token:
                return make_response(jsonify(message="Invalid access token"), 401)
            else:
                return make_response(learner.to_json(), 200, headers)
        except Exception as e:
            print(e)
            return make_response(jsonify(message="Incorrect URI or Internal error"), 500)

    @jwt_required()
    def delete(self, learner_id=None):
        try:
            token = request.headers.get('Authorization').split()[1]  # Get Bearer Token
            if find_learner_by_ID(learner_id) is None:
                return make_response(jsonify(message="Invalid learner ID"), 404)
            elif token != find_user_by_ID(learner_id).access_token:
                return make_response(jsonify(message="Invalid access token"), 401)
            else:
                delete_learner_by_ID(learner_id)
                return make_response(jsonify(message="Record deleted successfully!"), 200)
        except Exception as e:
            print(e)
            return make_response(jsonify(message="Incorrect URI or Incorrect URI or Internal error"), 500)

    def post(self):
        try:
            args = post_parser.parse_args()
        except Exception as e:
            print(e)
            return make_response(jsonify(message="Missing parameters!"), 401)
        learner_id = generate_id()
        create_learner(learner_id, args.first_name, args.last_name, args.email, args.education)
        access_token = create_user(learner_id, args.email, args.password)
        return make_response(jsonify({"message": "Record created successfully", "ID": learner_id,
                                      "Access Token": access_token, "status code": 200}), 200)

    @jwt_required()
    def patch(self, learner_id):
        try:
            args = patch_parser.parse_args()
            token = request.headers.get('Authorization').split()[1]  # Get Bearer Token
            if find_learner_by_ID(learner_id) is None:
                return make_response(jsonify(message="Invalid learner ID"), 404)
            elif token != find_user_by_ID(learner_id).access_token:
                return make_response(jsonify(message="Invalid access token"), 401)
            elif all(value is None for value in args.values()):  # checks if all args are None
                return make_response(jsonify(message="Nothing to update"), 200)
            else:
                learner = update_learner(learner_id, args.first_name, args.last_name, args.education)
                return make_response(learner.to_json(), 200, headers)
        except Exception as e:
            print(e)
            return make_response(jsonify(message="Incorrect URI or Internal error"), 500)
