from flask_mongoengine import MongoEngine
from services.CoursesService import initialize_courses
from services.LearnersService import initialize_learners


db = MongoEngine()


def initialize_db(app, course_db, learner_db):
    db.init_app(app)  # Create the db
    initialize_courses(course_db)  # Populate course db with default users
    initialize_learners(learner_db)  # Populate learner db with default users
