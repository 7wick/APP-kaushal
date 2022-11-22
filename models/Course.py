from mongoengine import Document, StringField, IntField


class Course(Document):
    course_id = IntField(required=True)
    title = StringField(max_length=100, required=True)
    watch_hours = IntField(required=True)
    level = StringField(max_length=100, required=True)
    email = StringField(max_length=100, required=True)
    views = IntField(required=False, default=0)
    watches = IntField(required=False, default=0)
    ratings = IntField(required=False, default=0)
    meta = {'db_alias': 'course-alias'}
