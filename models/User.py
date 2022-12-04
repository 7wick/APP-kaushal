from mongoengine import Document, StringField, IntField


class User(Document):
    user_id = IntField(max_length=10000, required=True)
    email = StringField(max_length=100, required=True)
    password_hash = StringField(required=True)
    access_token = StringField(default="", required=False)
    meta = {'db_alias': 'user-alias'}
