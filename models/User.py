from mongoengine import Document, StringField


class User(Document):
    email = StringField(max_length=100, required=True)
    password_hash = StringField(required=True)
    access_token = StringField(default="", required=False)
    meta = {'db_alias': 'user-alias'}
