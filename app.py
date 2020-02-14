from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required

from security import authenticate, identity
from user import SetProfile, GetProfile, UserRegister, AllMeds, CatCall, Search, AddOrder, Update

from delivery import Orders, Complete

from admin import NewMed, Up

from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'safety'
api = Api(app)

app.config['JWT_AUTH_URL_RULE'] = '/login'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=99999999999)

jwt = JWT(app, authenticate, identity)  # authentication

api.add_resource(UserRegister, '/sign_up')
api.add_resource(SetProfile, '/set_profile')
api.add_resource(GetProfile, '/get_profile')
api.add_resource(AllMeds, '/all_meds')
api.add_resource(CatCall, '/cat_call')
api.add_resource(Search, '/search')
api.add_resource(AddOrder, '/add_order')
api.add_resource(Update, '/update')

api.add_resource(Orders, '/orders')
api.add_resource(Complete, '/complete')

api.add_resource(Up, '/update')
api.add_resource(NewMed, '/new_med')

if __name__ == "__main__":
    app.run(port=5000, debug=True)
