from models.Course import Course
from mongoengine import *


def create_course(course_id, title, watch_hours, level, email, views, watches, ratings):
    new_course = Course(course_id=course_id, title=title, watch_hours=watch_hours, level=level, email=email, views=views,
                        watches=watches, ratings=ratings)
    new_course.save()
    return new_course


def all_courses():
    return Course.objects.all()


def find_course_by_ID(course_id):
    return Course.objects.filter(course_id=course_id).first()


def delete_course_by_ID(course_id):
    return Course.objects.filter(course_id=course_id).delete()


def update_course(course_id, title, watch_hours, level):
    course = Course.objects(course_id=course_id).first()
    if title is not None:
        course.title = title
    if watch_hours is not None:
        course.watch_hours = watch_hours
    if level is not None:
        course.level = level
    course.save()
    return course


def initialize_courses(database_name):  # Initialize the db with default courses
    disconnect(alias='course-alias')  # disconnect any existing connection
    database_connection = connect(database_name, alias='course-alias')
    database_connection.drop_database(database_name)  # erases all existing data

    Course(course_id=123451, title="fix taps", watch_hours=1, level="easy", email="course1@cmu.edu", views=1, watches=3,
           ratings=5).save()
    Course(course_id=123452, title="learn to paint", watch_hours=12, level="medium", email="course2@cmu.edu", views=12,
           watches=10, ratings=4).save()
    Course(course_id=123453, title="guitar lessons", watch_hours=30, level="hard", email="course3@cmu.edu", views=50,
           watches=35, ratings=2).save()
    Course(course_id=123454, title="fix a flat tire", watch_hours=1, level="medium", email="course4@cmu.edu", views=324,
           watches=350, ratings=5).save()

    database_connection.close()
    return "Data in {} database has been reset".format(database_name)

