from random import randrange
from flask import make_response, jsonify
from flask_restful import reqparse, Resource
from services.InstructorsService import *
import sys

post_parser = reqparse.RequestParser()
post_parser.add_argument('first_name', type=str, required=True, location='args')
post_parser.add_argument('last_name', type=str, required=True, location='args')
post_parser.add_argument('email', type=str, required=True, location='args')
# post_parser.add_argument('ssn', type=str, required=True, location='args')
# post_parser.add_argument('bank_routing_number', type=str, required=True, location='args')
# post_parser.add_argument('bank_account_number', type=str, required=True, location='args')

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
        except Exception:
            return make_response(jsonify(message="Database Empty!"), 404)


class Instructor(Resource):
    def get(self, instructor_id=None):
        try:
            if find_instructor_by_ID(instructor_id) is not None:
                instructor = find_instructor_by_ID(instructor_id)
                return make_response(instructor.to_json(), 200, headers)
            else:
                return make_response(jsonify(message="Invalid instructor ID"), 404)
        except Exception:
            return make_response(jsonify(message="Incorrect URI"), 401)

    def delete(self, instructor_id=None):
        try:
            if find_instructor_by_ID(instructor_id):
                delete_instructor_by_ID(instructor_id)
                return make_response(jsonify(message="Record deleted successfully!"), 200)
            else:
                return make_response(jsonify(message="Invalid instructor ID!"), 404)
        except Exception:
            return make_response(jsonify(message="Incorrect URI"), 401)

    def post(self):
        instructor_id = sys.maxsize  # setting max integer as default instructor_id
        try:
            args = post_parser.parse_args()
        except Exception:
            return make_response(jsonify(message="Missing parameters!"), 401)
        generated_flag = True
        while generated_flag:
            instructor_id = randrange(1000, 9999)
            if find_instructor_by_ID(instructor_id) is None:
                generated_flag = False
        create_instructor(instructor_id, args.first_name, args.last_name, args.email)
        return make_response(jsonify(message="Record created successfully. Record ID is: {}".format(instructor_id)), 200)

    def patch(self, instructor_id):
        try:
            args = patch_parser.parse_args()
            if all(value is None for value in args.values()):  # checks if all args are None
                return make_response(jsonify(message="Nothing to update"), 200)
            if find_instructor_by_ID(instructor_id):
                instructor = update_instructor(instructor_id, args.first_name, args.last_name)
                return make_response(instructor.to_json(), 200, headers)
            else:
                return make_response(jsonify(message="Invalid instructor ID"), 404)
        except Exception:
            return make_response(jsonify(message="Incorrect URI"), 401)
