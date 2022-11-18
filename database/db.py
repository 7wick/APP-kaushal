from flask_mongoengine import MongoEngine
from services.CoursesService import reset_courses


db = MongoEngine()


def initialize_db(app, db_name):
    db.init_app(app)  # Create the db
    reset_courses(db_name)  # Populate it with default users
    # init_riders()  # Populate it with default riders
