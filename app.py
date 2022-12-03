from flask import Flask
from flask_jwt_extended import JWTManager
from jwt import exceptions as jwt_exception
from flask_restful import Api
from database.db import initialize_db
from utils.JSONEncoder import MongoEngineJSONEncoder
from resources.Course import *
from resources.Learner import *
import resources
from resources.Instructor import *
from resources.Bank import *
# from resources.Sessions import *
from resources.User import *

app = Flask(__name__)  # Creating a FLASK app
course_db = "kaushal-courses"
learner_db = "kaushal-learners"
instructor_db = "kaushal-instructors"
bank_db = "kaushal-bank"
user_db = "kaushal-user"
host = 'mongodb://localhost:27017/'

app.config['MONGODB_SETTINGS'] = [
    {
        'alias': 'course-alias',
        'db': course_db,
        'host': host
    },
    {
        'alias': 'learner-alias',
        'db': learner_db,
        'host': host
    },
    {
        'alias': 'instructor-alias',
        'db': instructor_db,
        'host': host
    },
    {
        'alias': 'bank-alias',
        'db': bank_db,
        'host': host
    },
    {
        'alias': 'user-alias',
        'db': user_db,
        'host': host
    }
]

jwt = JWTManager(app)
app.json_encoder = MongoEngineJSONEncoder

app.config['JWT_SECRET_KEY'] = 'do-not-breach-my-privacy'  # Change this!
app.config['PROPAGATE_EXCEPTIONS'] = True

initialize_db(app, course_db, learner_db, instructor_db, bank_db, user_db)  # create and initialize databases

api = Api(app)  # Creating a REST API for the app

# api.add_resource(Sessions, '/sessions/')
api.add_resource(Users, '/users/')
api.add_resource(User, '/user/<string:user_email>/')

api.add_resource(Courses, '/courses/')
api.add_resource(Course,
                 '/course/',
                 '/course/<string:course_id>/')

api.add_resource(Learners, '/learners/')
api.add_resource(resources.Learner.Learner,
                 '/learner/',
                 '/learner/<string:learner_id>/')

api.add_resource(Instructors, '/instructors/')
api.add_resource(Instructor,
                 '/instructor/',
                 '/instructor/<string:instructor_id>/')

api.add_resource(Banks, '/bank_accounts/')
api.add_resource(Bank,
                 '/instructor/<string:instructor_id>/bank_account/',
                 '/instructor/<string:instructor_id>/bank_account/<string:bank_account_id>/')


@app.route('/')
def hello_world():
    raise jwt_exception.ExpiredSignatureError


if __name__ == "__main__":
    app.run()  # Runs web app @ http://localhost:5000 by default for me.
