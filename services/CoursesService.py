from models.Course import Course
from mongoengine import *


def create_course(title, course_id, watch_hours, level, email, views, watches, ratings):
    new_course = Course(title=title, ID=course_id, watch_hours=watch_hours, level=level, email=email, views=views,
                        watches=watches, ratings=ratings)
    new_course.save()
    return new_course


def all_courses():
    return Course.objects.all()


def find_course_by_ID(course_id):
    return Course.objects.filter(ID=course_id).first()


def delete_course_by_ID(course_id):
    return Course.objects.filter(ID=course_id).delete()


def update_rider(course_id, title, watch_hours, level):
    course = Course.objects(ID=course_id).first()
    course.update(title=title, watch_hours=watch_hours, level=level)
    course.reload()  # Get the latest copy from the db
    return course  # Return the list of one rider object that was updated


def reset_courses(database_name):  # Initialize the db with default courses
    disconnect()  # disconnect any existing connection
    database_connection = connect(database_name)
    database_connection.drop_database(database_name)  # erases all existing data

    Course(title="title1", ID=123451, watch_hours=1, level="level1", email="email1@cmu.edu", views=1, watches=1,
           ratings=2).save()
    Course(title="title2", ID=123452, watch_hours=12, level="level2", email="email2@cmu.edu", views=12, watches=10,
           ratings=4).save()
    Course(title="title3", ID=123459, watch_hours=3, level="level3", email="email3@cmu.edu", views=50, watches=35,
           ratings=5).save()

    database_connection.close()
    return "Data in {} database has been reset".format(database_name)

