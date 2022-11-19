from random import randrange
from flask import abort, make_response, jsonify
from flask_restful import reqparse, Resource
from services.CoursesService import *

post_parser = reqparse.RequestParser()
post_parser.add_argument('title', type=str)
post_parser.add_argument('watch_hours', type=int)
post_parser.add_argument('level', type=str)
post_parser.add_argument('email', type=str)
post_parser.add_argument('views', type=int)
post_parser.add_argument('watches', type=int)
post_parser.add_argument('ratings', type=int)

patch_parser = reqparse.RequestParser()
patch_parser.add_argument('title', type=str)
patch_parser.add_argument('watch_hours', type=int)
patch_parser.add_argument('level', type=str)

headers = {'Content-Type': 'application/json'}


class Courses(Resource):
    def get(self):
        try:
            courses = all_courses()
            return make_response(courses.to_json(), 200, headers)
        except:
            return abort(403, "Database Empty!")


class Course(Resource):
    def get(self, course_id=None):
        try:
            if find_course_by_ID(course_id):
                course = find_course_by_ID(course_id)
                return make_response(course.to_json(), 200, headers)
            else:
                return abort(404, "Invalid course ID")
        except:
            return make_response(jsonify(message="Incorrect URI"), 404)

    def delete(self, course_id=None):
        try:
            if find_course_by_ID(course_id):
                delete_course_by_ID(course_id)
                return make_response(jsonify(message="Record deleted successfully!"), 200)
            else:
                return abort(404, "Invalid course ID")
        except:
            return make_response(jsonify(message="Incorrect URI"), 404)

    def post(self):
        course_id = 999999
        try:
            args = post_parser.parse_args()
        except Exception as e:
            return abort(400, "Missing parameters!")
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
            if find_course_by_ID(course_id):
                course = update_rider(course_id, args.title, args.watch_hours, args.level)
                return make_response(course.to_json(), 200, headers)
            else:
                return abort(404, "Invalid course ID")
        except:
            return make_response(jsonify(message="Incorrect URI"), 404)
