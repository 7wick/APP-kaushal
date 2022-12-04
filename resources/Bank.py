from flask import make_response, jsonify
from flask_restful import reqparse, Resource
from services.BanksService import *
from services.UsersService import generate_id

post_parser = reqparse.RequestParser()
post_parser.add_argument('ssn', type=str, required=True, location='args')
post_parser.add_argument('bank_routing_number', type=str, required=True, location='args')
post_parser.add_argument('bank_account_number', type=str, required=True, location='args')

patch_parser = reqparse.RequestParser()
patch_parser.add_argument('bank_routing_number', type=str, location='form')
patch_parser.add_argument('bank_account_number', type=str, location='form')

get_banks_parser = reqparse.RequestParser()
get_banks_parser.add_argument('pagesize', type=int, location='args')
get_banks_parser.add_argument('page', type=int, location='args')

headers = {'Content-Type': 'application/json'}


class Banks(Resource):
    def get(self, pagesize=None, page=None):
        try:
            args = get_banks_parser.parse_args()
            accounts = all_banks()
            if not all(value is None for value in args.values()):
                if args.page is None:
                    args.page = 1  # default page
                if args.pagesize is None:
                    args.pagesize = 5  # default pagesize
                start = (args.page - 1)*args.pagesize
                end = args.page*args.pagesize
                if start > end:
                    return make_response(jsonify(message="pagination values incorrect!"), 401)
                accounts = accounts[start:end]  # pagination
                if not len(accounts):
                    return make_response(jsonify(message="No data for current pagination"), 404)
            return make_response(accounts.to_json(), 200, headers)
        except Exception:
            return make_response(jsonify(message="Database Empty!"), 404)


class Bank(Resource):
    def get(self, instructor_id=None, bank_account_id=None):
        try:
            if bank_account_id is None:
                if find_bank_by_instructor(instructor_id) is not None:
                    account = find_bank_by_instructor(instructor_id)
                    return make_response(account.to_json(), 200, headers)
                else:
                    return make_response(jsonify(message="Invalid instructor ID"), 404)
            else:
                if find_bank_by_account(bank_account_id) is not None:
                    account = find_bank_by_account(bank_account_id)
                    return make_response(account.to_json(), 200, headers)
                else:
                    return make_response(jsonify(message="Invalid account ID"), 404)
        except Exception as e:
            print(e)
            return make_response(jsonify(message="Incorrect URI or Internal error"), 500)

    def delete(self, instructor_id=None, bank_account_id=None):
        try:
            if find_bank_by_account(bank_account_id):
                delete_bank_by_account(bank_account_id)
                return make_response(jsonify(message="Record deleted successfully!"), 200)
            else:
                return make_response(jsonify(message="Invalid account ID!"), 404)
        except Exception as e:
            print(e)
            return make_response(jsonify(message="Incorrect URI or Internal error"), 500)

    def post(self, instructor_id=None):
        if find_bank_by_instructor(instructor_id) is None:
            return make_response(jsonify(message="Instructor with {} id doesn't exists".format(instructor_id)), 401)
        try:
            args = post_parser.parse_args()
        except Exception as e:
            print(e)
            return make_response(jsonify(message="Missing parameters!"), 401)
        try:
            bank_account_id = generate_id()
            create_bank_account(bank_account_id, instructor_id, args.ssn, args.bank_routing_number,
                                args.bank_account_number)
            return make_response(jsonify(message="Record created successfully. Record ID is: {}".format(bank_account_id))
                                 , 200)
        except Exception as e:
            print(e)
            return make_response(jsonify(message="Incorrect URI or Internal error"), 500)

    def patch(self, instructor_id=None, bank_account_id=None):
        if find_bank_by_instructor(instructor_id) is None:
            return make_response(jsonify(message="Instructor with {} id doesn't exists".format(instructor_id)), 401)
        if find_bank_by_account(bank_account_id) is None:
            return make_response(jsonify(message="Bank with {} id doesn't exists".format(bank_account_id)), 401)
        try:
            args = patch_parser.parse_args()
            if all(value is None for value in args.values()):  # checks if all args are None
                return make_response(jsonify(message="Nothing to update"), 200)
            if find_bank_by_account(bank_account_id):
                account = update_account(bank_account_id, args.bank_routing_number, args.bank_account_number)
                return make_response(account.to_json(), 200, headers)
            else:
                return make_response(jsonify(message="Invalid account ID"), 404)
        except Exception as e:
            print(e)
            return make_response(jsonify(message="Incorrect URI or Internal error"), 500)
