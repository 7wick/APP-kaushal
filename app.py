from flask import Flask
from flask_restful import Api
from database.db import initialize_db
from utils.JSONEncoder import MongoEngineJSONEncoder
from resources.Course import *
from resources.Learner import *
from resources.Instructor import *

app = Flask(__name__)  # Creating a FLASK app
course_db = "kaushal-courses"
learner_db = "kaushal-learners"
instructor_db = "kaushal-instructors"
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
    }
]


initialize_db(app, course_db, learner_db, instructor_db)   # create and initialize database
app.json_encoder = MongoEngineJSONEncoder
api = Api(app)  # Creating a REST API for the app

api.add_resource(Courses, '/courses/')
api.add_resource(Course,
                 '/course/',
                 '/course/<string:course_id>/')

api.add_resource(Learners, '/learners/')
api.add_resource(Learner,
                 '/learner/',
                 '/learner/<string:learner_id>/')

api.add_resource(Instructors, '/instructors/')
api.add_resource(Instructor,
                 '/instructor/',
                 '/instructor/<string:instructor_id>/')

if __name__ == "__main__":
    app.run()  # Runs web app @ http://localhost:5000 by default for me.
