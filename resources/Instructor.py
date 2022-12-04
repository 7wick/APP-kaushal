from flask import make_response, jsonify, request
from flask_jwt_extended import jwt_required
from flask_restful import reqparse, Resource
from services.InstructorsService import *
from services.UsersService import generate_id

post_parser = reqparse.RequestParser()
post_parser.add_argument('first_name', type=str, required=True, location='args')
post_parser.add_argument('last_name', type=str, required=True, location='args')
post_parser.add_argument('email', type=str, required=True, location='args')
post_parser.add_argument('password', type=str, required=True, location='args')

patch_parser = reqparse.RequestParser()
patch_parser.add_argument('first_name', type=str, location='form')
patch_parser.add_argument('last_name', type=str, location='form')

get_instructors_parser = reqparse.RequestParser()
get_instructors_parser.add_argument('pagesize', type=int, location='args')
get_instructors_parser.add_argument('page', type=int, location='args')

headers = {'Content-Type': 'application/json'}


class Instructors(Resource):
    def get(self, pagesize=None, page=None):
        try:
            args = get_instructors_parser.parse_args()
            instructors = all_instructors()
            if not all(value is None for value in args.values()):
                if args.page is None:
                    args.page = 1  # default page
                if args.pagesize is None:
                    args.pagesize = 5  # default pagesize
                start = (args.page - 1)*args.pagesize
                end = args.page*args.pagesize
                if start > end:
                    return make_response(jsonify(message="pagination values incorrect!"), 401)
                instructors = instructors[start:end]  # pagination
                if not len(instructors):
                    return make_response(jsonify(message="No data for current pagination"), 404)
            return make_response(instructors.to_json(), 200, headers)
        except Exception as e:
            print(e)
            return make_response(jsonify(message="Database Empty!"), 404)


class Instructor(Resource):
    @jwt_required()
    def get(self, instructor_id=None):
        try:
            instructor = find_instructor_by_ID(instructor_id)
            if instructor is None:
                return make_response(jsonify(message="Invalid instructor ID"), 404)
            else:
                token = request.headers.get('Authorization').split()[1]  # Get Bearer Token
                if token != find_user_by_ID(instructor_id).access_token:
                    return make_response(jsonify(message="Invalid access token"), 401)
                else:
                    return make_response(instructor.to_json(), 200, headers)
        except Exception as e:
            print(e)
            return make_response(jsonify(message="Incorrect URI or Internal error"), 500)

    @jwt_required()
    def delete(self, instructor_id=None):
        try:
            if find_instructor_by_ID(instructor_id) is None:
                return make_response(jsonify(message="Invalid instructor ID"), 404)
            else:
                token = request.headers.get('Authorization').split()[1]  # Get Bearer Token
                if token != find_user_by_ID(instructor_id).access_token:
                    return make_response(jsonify(message="Invalid access token"), 401)
                else:
                    delete_instructor_by_ID(instructor_id)
                    return make_response(jsonify(message="Record deleted successfully!"), 200)
        except Exception as e:
            print(e)
            return make_response(jsonify(message="Incorrect URI or Internal error"), 500)

    def post(self):
        try:
            args = post_parser.parse_args()
        except Exception as e:
            print(e)
            return make_response(jsonify(message="Missing parameters!"), 401)
        instructor_id = generate_id()
        create_instructor(instructor_id, args.first_name, args.last_name, args.email)
        access_token = create_user(instructor_id, args.email, args.password)
        return make_response(jsonify({"message": "Record created successfully", "ID": instructor_id,
                                      "Access Token": access_token, "status code": 200}), 200)

    @jwt_required()
    def patch(self, instructor_id):
        try:
            args = patch_parser.parse_args()
            if find_instructor_by_ID(instructor_id) is None:
                return make_response(jsonify(message="Invalid instructor ID"), 404)
            else:
                token = request.headers.get('Authorization').split()[1]  # Get Bearer Token
                if token != find_user_by_ID(instructor_id).access_token:
                    return make_response(jsonify(message="Invalid access token"), 401)
                else:
                    if all(value is None for value in args.values()):  # checks if all args are None
                        return make_response(jsonify(message="Nothing to update"), 200)
                    else:
                        instructor = update_instructor(instructor_id, args.first_name, args.last_name)
                        return make_response(instructor.to_json(), 200, headers)
        except Exception as e:
            print(e)
            return make_response(jsonify(message="Incorrect URI or Internal error"), 500)
