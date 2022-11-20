from random import randrange
from flask import make_response, jsonify
from flask_restful import reqparse, Resource
from services.CoursesService import *
import sys

post_parser = reqparse.RequestParser()
post_parser.add_argument('title', type=str, required=True, location='args')
post_parser.add_argument('watch_hours', type=int, required=True, location='args')
post_parser.add_argument('level', type=str, required=True, location='args')
post_parser.add_argument('email', type=str, required=True, location='args')
post_parser.add_argument('views', type=int, location='args')
post_parser.add_argument('watches', type=int, location='args')
post_parser.add_argument('ratings', type=int, location='args')

patch_parser = reqparse.RequestParser()
patch_parser.add_argument('title', type=str, location='form')
patch_parser.add_argument('watch_hours', type=int, location='form')
patch_parser.add_argument('level', type=str, location='form')

headers = {'Content-Type': 'application/json'}


class Courses(Resource):
    def get(self):
        try:
            courses = all_courses()
            return make_response(courses.to_json(), 200, headers)
        except:
            return make_response(jsonify(message="Database Empty!"), 404)


class Course(Resource):
    def get(self, course_id=None):
        try:
            if find_course_by_ID(course_id) is not None:
                course = find_course_by_ID(course_id)
                return make_response(course.to_json(), 200, headers)
            else:
                return make_response(jsonify(message="Invalid course ID"), 404)
        except Exception as e:
            return make_response(jsonify(message="Incorrect URI"), 401)

    def delete(self, course_id=None):
        try:
            if find_course_by_ID(course_id):
                delete_course_by_ID(course_id)
                return make_response(jsonify(message="Record deleted successfully!"), 200)
            else:
                return make_response(jsonify(message="Invalid course ID!"), 404)
        except:
            return make_response(jsonify(message="Incorrect URI"), 401)

    def post(self):
        course_id = sys.maxsize  # setting max integer as default course_if
        try:
            args = post_parser.parse_args()
        except Exception:
            return make_response(jsonify(message="Missing parameters!"), 401)
        generated_flag = True
        while generated_flag:
            course_id = randrange(100000, 999999)
            if find_course_by_ID(course_id) is None:
                generated_flag = False
        create_course(args.title, course_id, args.watch_hours, args.level, args.email, args.views, args.watches,
                      args.ratings)
        return make_response(jsonify(message="Record created successfully!"), 200)

    def patch(self, course_id):
        try:
            args = patch_parser.parse_args()
            if all(value is None for value in args.values()):
                return make_response(jsonify(message="Nothing to update"), 200)
            if find_course_by_ID(course_id):
                course = update_rider(course_id, args.title, args.watch_hours, args.level)
                return make_response(course.to_json(), 200, headers)
            else:
                return make_response(jsonify(message="Invalid course ID"), 404)
        except:
            return make_response(jsonify(message="Incorrect URI"), 401)
