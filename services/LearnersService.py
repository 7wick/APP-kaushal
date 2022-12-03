from models.Learner import Learner
from services.UsersService import *


def create_learner(learner_id, first_name, last_name, email, education):
    new_learner = Learner(learner_id=learner_id, first_name=first_name, last_name=last_name, email=email, education=education)
    new_learner.save()
    return new_learner


def all_learners():
    return Learner.objects.all()


def find_learner_by_ID(learner_id):
    return Learner.objects.filter(learner_id=learner_id).first()


def delete_learner_by_ID(learner_id):
    delete_user(delete_learner_by_ID(learner_id).email)
    return Learner.objects.filter(learner_id=learner_id).delete()


def update_learner(learner_id, first_name, last_name, education):
    learner = Learner.objects(learner_id=learner_id).first()
    if first_name is not None:
        learner.first_name = first_name
    if last_name is not None:
        learner.last_name = last_name
    if education is not None:
        learner.education = education
    learner.save()
    return learner


def initialize_learners(database_name):  # Initialize the db with default learners
    disconnect(alias='learner-alias')  # disconnect any existing connection
    database_connection = connect(database_name, alias='learner-alias')
    database_connection.drop_database(database_name)  # erases all existing data

    Learner(learner_id=1231, first_name="Heer", last_name="Kaul", email="learner1@cmu.edu",
            education="high school").save()
    Learner(learner_id=1232, first_name="Jordan", last_name="Jackson", email="learner2@cmu.edu",
            education="undergraduate").save()
    Learner(learner_id=1233, first_name="Jordan", last_name="Mishra", email="learner3@cmu.edu",
            education="graduate").save()
    Learner(learner_id=1234, first_name="Shivali", last_name="Mittal", email="learner4@cmu.edu",
            education="no school").save()

    database_connection.close()
    return "Data in {} learner database has been reset".format(database_name)
