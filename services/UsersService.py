from models.User import User
from utils.Hash import get_hash
from mongoengine import *
from flask_jwt_extended import create_access_token
from datetime import timedelta
from random import randrange


def create_user(user_id, email, password):
    password_hash = get_hash(password.encode('utf-8'))
    user = User(user_id=user_id, email=email, password_hash=password_hash)
    user.save()
    access_token = update_token(email)
    return access_token


def update_token(email):
    user = User.objects.filter(email=email).first()
    access_token = create_access_token(identity=email, expires_delta=timedelta(minutes=100))
    user.access_token = access_token
    user.save()
    return access_token


def generate_id():
    global user_id
    generated_flag = True
    while generated_flag:
        user_id = randrange(1000, 9999)
        if find_user_by_ID(user_id) is None:
            generated_flag = False
    return user_id


def delete_user(email):
    return User.objects.filter(email=email).delete()


def find_user_by_email(email):
    return User.objects.filter(email=email).first()


def find_user_by_ID(user_id):
    return User.objects.filter(user_id=user_id).first()


def all_users():
    return User.objects.all()


def initialize_users(database_name):  # Initialize the db with default users
    disconnect(alias='user-alias')  # disconnect any existing connection
    database_connection = connect(database_name, alias='user-alias')
    database_connection.drop_database(database_name)  # erases all existing data

    User(user_id=1001, email="learner1@cmu.edu", password_hash="c405872826fabf3179cc7f603e001d1e",
         access_token=create_access_token(identity="learner1@cmu.edu", expires_delta=timedelta(minutes=100))).save()
    User(user_id=1002, email="learner2@cmu.edu", password_hash="e3c527014c229e326c71afa0c38a6f9b",
         access_token=create_access_token(identity="learner2@cmu.edu", expires_delta=timedelta(minutes=100))).save()
    User(user_id=1003, email="learner3@cmu.edu", password_hash="a2ce2bb147bd202c7b36bf183e530a4c",
         access_token=create_access_token(identity="learner3@cmu.edu", expires_delta=timedelta(minutes=100))).save()
    User(user_id=1004, email="learner4@cmu.edu", password_hash="373dcc1c8812a026f65e317a02fb5dee",
         access_token=create_access_token(identity="learner4@cmu.edu", expires_delta=timedelta(minutes=100))).save()
    User(user_id=1005, email="instructor1@cmu.edu", password_hash="fd42e20bcb1417e84e789d8232190ae5",
         access_token=create_access_token(identity="instructor1@cmu.edu", expires_delta=timedelta(minutes=100))).save()
    User(user_id=1006, email="instructor2@cmu.edu", password_hash="ab9fcb283298bed333d094f85f0c6c86",
         access_token=create_access_token(identity="instructor2@cmu.edu", expires_delta=timedelta(minutes=100))).save()
    User(user_id=1007, email="instructor3@cmu.edu", password_hash="4836ffb6bcd0ebaa9af8d90bd14c5783",
         access_token=create_access_token(identity="instructor3@cmu.edu", expires_delta=timedelta(minutes=100))).save()
    User(user_id=1008, email="instructor4@cmu.edu", password_hash="9027d6215a79e180202e704e255c5625",
         access_token=create_access_token(identity="instructor4@cmu.edu", expires_delta=timedelta(minutes=100))).save()

    database_connection.close()
    return "Data in {} database has been reset".format(database_name)
