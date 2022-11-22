from mongoengine import Document, StringField, IntField


class Learner(Document):
    learner_id = IntField(required=True)
    first_name = StringField(max_length=100, required=True)
    last_name = StringField(max_length=100, required=True)
    email = StringField(max_length=100, required=True)
    education = StringField(required=False, default="")
    meta = {'db_alias': 'learner-alias'}
