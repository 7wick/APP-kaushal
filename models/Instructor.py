from mongoengine import Document, StringField, IntField


class Instructor(Document):
    instructor_id = IntField(required=True)
    first_name = StringField(max_length=100, required=True)
    last_name = StringField(max_length=100, required=True)
    email = StringField(max_length=100, required=True)
    meta = {'db_alias': 'instructor-alias'}
