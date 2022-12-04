from models.Instructor import Instructor
from services.UsersService import *


def create_instructor(instructor_id, first_name, last_name, email):
    new_instructor = Instructor(instructor_id=instructor_id, first_name=first_name, last_name=last_name, email=email)
    new_instructor.save()
    return new_instructor


def all_instructors():
    return Instructor.objects.all()


def find_instructor_by_ID(instructor_id):
    return Instructor.objects.filter(instructor_id=instructor_id).first()


def delete_instructor_by_ID(instructor_id):
    delete_user(find_instructor_by_ID(instructor_id).email)
    return Instructor.objects.filter(instructor_id=instructor_id).delete()


def update_instructor(instructor_id, first_name, last_name):
    instructor = Instructor.objects(instructor_id=instructor_id).first()
    if first_name is not None:
        instructor.first_name = first_name
    if last_name is not None:
        instructor.last_name = last_name
    instructor.save()
    return instructor


def initialize_instructors(database_name):  # Initialize the db with default instructors
    disconnect(alias='instructor-alias')  # disconnect any existing connection
    database_connection = connect(database_name, alias='instructor-alias')
    database_connection.drop_database(database_name)  # erases all existing data

    Instructor(instructor_id=1005, first_name="Rahul", last_name="Kedia", email="instructor1@cmu.edu").save()
    Instructor(instructor_id=1006, first_name="Bhavya", last_name="Paliwal", email="instructor2@cmu.edu").save()
    Instructor(instructor_id=1007, first_name="Jake", last_name="Perry", email="instructor3@cmu.edu").save()
    Instructor(instructor_id=1008, first_name="Shiv", last_name="Nadar", email="instructor4@cmu.edu").save()

    database_connection.close()
    return "Data in {} instructor database has been reset".format(database_name)

