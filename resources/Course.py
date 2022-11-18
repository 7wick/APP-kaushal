from flask import abort, make_response, jsonify
from flask_restful import reqparse, Resource
from services.CoursesService import *

post_parser = reqparse.RequestParser()
post_parser.add_argument('title', type=str, default="")
post_parser.add_argument('watch_hours', type=int, default=0)
post_parser.add_argument('level', type=str, default="")
post_parser.add_argument('email', type=str, default="")
post_parser.add_argument('views', type=int, default=0)
post_parser.add_argument('watches', type=int, default=0)
post_parser.add_argument('ratings', type=int, default=0)

patch_parser = reqparse.RequestParser()
patch_parser.add_argument('title', type=str, default="")
post_parser.add_argument('watch_hours', type=int, default=0)
post_parser.add_argument('level', type=str, default="")

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
        if find_course_by_ID(course_id):
            course = find_course_by_ID(course_id)
            return make_response(course.to_json(), 200, headers)
        else:
            return abort(404, "Invalid course ID")

    def delete(self, course_id=None):
        if find_course_by_ID(course_id):
            delete_course_by_ID(course_id)
            return make_response(jsonify(message="Record deleted successfully!"), 200)
        else:
            return abort(404, "Invalid course ID")


    def post(self):
        args = post_parser.parse_args()
    #     if len(args.name) == 0 or len(args.email) == 0:
    #         abort(400, "ERROR! name and email are required fields.")
    #     elif email_identity == args.email:
    #         found_rider = get_rider_by_email(args.email)
    #         if found_rider is None:
    #             response = create_rider(args.name, args.email, args.premium)
    #             return make_response(response.to_json(), 200, headers)
    #         else:
    #             abort(400, "ERROR! Rider with this email already exists.")
    #     else:
    #         return abort(403)

    # def patch(self, rider_id):
    #     email_identity = get_jwt_identity()
    #     rider = get_rider_by_id(rider_id)
    #     if rider and email_identity == rider.email:
    #         args = patch_parser.parse_args()
    #         rider = update_rider(rider_id, args.premium)
    #         return make_response(rider.to_json(), 200, headers)
    #     else:
    #         abort(403)

