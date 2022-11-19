from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
# from jwt import exceptions as jwt_exception

from database.db import initialize_db
from utils.JSONEncoder import MongoEngineJSONEncoder
from resources.Course import Course, Courses

app = Flask(__name__)  # Creating a FLASK app
db_name = 'app-kaushal'
host = 'mongodb://localhost:27017/' + db_name

app.config['MONGODB_SETTINGS'] = {
    'db': db_name,
    'host': host
}

# app.config['JWT_SECRET_KEY'] = 'lets-give-fake-data-to-internet'  # Change this!
# app.config['PROPAGATE_EXCEPTIONS'] = True

initialize_db(app, db_name)   # create and initialize database
# jwt = JWTManager(app)
app.json_encoder = MongoEngineJSONEncoder
api = Api(app)  # Creating a REST API for the app

# http://localhost:5000/rider
# http://localhost:5000/rider/rider_id
# http://localhost:5000/rider/rider_id?arg=value
api.add_resource(Course,
                 '/course', '/course/',
                 '/course/<string:course_id>', '/course/<string:course_id>/')

api.add_resource(Courses, '/courses', '/courses/')

if __name__ == "__main__":
    app.run()  # Runs web app @ http://localhost:5000 by default for me.
