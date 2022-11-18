from mongoengine import Document, StringField, IntField


class Course(Document):
    title = StringField(max_length=100, required=True)
    ID = IntField(required=True)
    watch_hours = IntField(required=True)
    level = StringField(max_length=100, required=True)
    email = StringField(max_length=100, required=True)
    views = IntField(required=False)
    watches = IntField(required=False)
    ratings = IntField(required=False)
