from mongoengine import Document, StringField, IntField


class Course(Document):
    title = StringField(max_length=100, required=True)
    ID = IntField(required=True)
    watch_hours = IntField(required=True)
    level = StringField(max_length=100, required=True)
    email = StringField(max_length=100, required=True)
    views = IntField(required=False, default=0)
    watches = IntField(required=False, default=0)
    ratings = IntField(required=False, default=0)
