from models.Instructor import Instructor
from mongoengine import *


def create_instructor(instructor_id, first_name, last_name, email):
    new_instructor = Instructor(instructor_id=instructor_id, first_name=first_name, last_name=last_name, email=email)
    new_instructor.save()
    return new_instructor


def all_instructors():
    return Instructor.objects.all()


def find_instructor_by_ID(instructor_id):
    return Instructor.objects.filter(instructor_id=instructor_id).first()


def delete_instructor_by_ID(instructor_id):
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

    Instructor(instructor_id=121, first_name="Rahul", last_name="Kedia", email="instructor1@cmu.edu").save()
    Instructor(instructor_id=122, first_name="Bhavya", last_name="Paliwal", email="instructor2@cmu.edu").save()
    Instructor(instructor_id=123, first_name="Jake", last_name="Perry", email="instructor3@cmu.edu").save()
    Instructor(instructor_id=124, first_name="Shiv", last_name="Nadar", email="instructor4@cmu.edu").save()
    #
    # Instructor(instructor_id=121, first_name="Rahul", last_name="Kedia", email="instructor1@cmu.edu", ssn="sadahdgj",
    #            bank_routing_number="12345", bank_account_number="bofa123").save()
    # Instructor(instructor_id=122, first_name="Bhavya", last_name="Paliwal", email="instructor2@cmu.edu", ssn="lkljlkf",
    #            bank_routing_number="86749", bank_account_number="chase959").save()
    # Instructor(instructor_id=123, first_name="Jake", last_name="Perry", email="instructor3@cmu.edu", ssn="etertr",
    #            bank_routing_number="98798", bank_account_number="bofa09900").save()
    # Instructor(instructor_id=124, first_name="Shiv", last_name="Nadar", email="instructor4@cmu.edu", ssn="bnfbgd",
    #            bank_routing_number="12342", bank_account_number="pnc323").save()

    database_connection.close()
    return "Data in {} instructor database has been reset".format(database_name)

