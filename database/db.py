from flask_mongoengine import MongoEngine
from services.CoursesService import initialize_courses


db = MongoEngine()


def initialize_db(app, db_name):
    db.init_app(app)  # Create the db
    initialize_courses(db_name)  # Populate it with default users
