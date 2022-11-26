from models.Bank import Bank
from mongoengine import *


def create_bank_account(bank_account_id, instructor_id, ssn, bank_routing_number, bank_account_number):
    new_bank_account = Bank(bank_account_id=bank_account_id, instructor_id=instructor_id, ssn=ssn,
                            bank_routing_number=bank_routing_number, bank_account_number=bank_account_number)
    new_bank_account.save()
    return new_bank_account


def all_banks():
    return Bank.objects.all()


def find_bank_by_instructor(instructor_id):
    return Bank.objects.filter(instructor_id=instructor_id)


def find_bank_by_account(bank_account_id):
    return Bank.objects.filter(bank_account_id=bank_account_id).first()


def delete_bank_by_account(bank_account_id):
    return Bank.objects.filter(bank_account_id=bank_account_id).delete()


def update_account(bank_account_id, bank_routing_number, bank_account_number):
    account = Bank.objects(bank_account_id=bank_account_id).first()
    if bank_routing_number is not None:
        account.bank_routing_number = bank_routing_number
    if bank_account_number is not None:
        account.bank_account_number = bank_account_number
    account.save()
    return account


def initialize_bank_accounts(database_name):  # Initialize the db with default bank accounts
    disconnect(alias='bank-alias')  # disconnect any existing connection
    database_connection = connect(database_name, alias='bank-alias')
    database_connection.drop_database(database_name)  # erases all existing data

    Bank(instructor_id=121, bank_account_id=9121, ssn="ssn121", bank_routing_number="12345",
         bank_account_number="bofa123").save()
    Bank(instructor_id=122, bank_account_id=9122, ssn="ssn122", bank_routing_number="86749",
         bank_account_number="chase959").save()
    Bank(instructor_id=123, bank_account_id=9123, ssn="ssn123", bank_routing_number="12345",
         bank_account_number="wellsfargo453").save()
    Bank(instructor_id=124, bank_account_id=9124, ssn="ssn124", bank_routing_number="86749",
         bank_account_number="pnc323").save()

    database_connection.close()
    return "Data in {} instructor database has been reset".format(database_name)

