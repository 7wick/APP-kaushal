from flask_mongoengine import MongoEngine
from services.CoursesService import initialize_courses
from services.LearnersService import initialize_learners
from services.InstructorsService import initialize_instructors
from services.BanksService import initialize_bank_accounts

db = MongoEngine()


def initialize_db(app, course_db, learner_db, instructor_db, bank_db):
    db.init_app(app)  # Create the db
    initialize_courses(course_db)  # Populate course db with default records
    initialize_learners(learner_db)  # Populate learner db with default records
    initialize_instructors(instructor_db)  # Populate instructor db with default records
    initialize_bank_accounts(bank_db)  # Populate bank db with default records
