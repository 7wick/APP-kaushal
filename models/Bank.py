from mongoengine import Document, StringField, IntField


class Bank(Document):
    instructor_id = IntField(required=True)
    bank_account_id = IntField(required=True)
    ssn = StringField(max_length=100, required=True)
    bank_routing_number = StringField(max_length=100, required=True)
    bank_account_number = StringField(max_length=100, required=True)
    meta = {'db_alias': 'bank-alias'}
