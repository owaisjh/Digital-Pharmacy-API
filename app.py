from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required

from security import authenticate, identity
from user import SetProfile, GetProfile, UserRegister, AllMeds, CatCall, Search, AddOrder, DecStock, ListOrders, PresOrder, ForgetPassword,CheckUser

from delivery import Orders, Complete

from admin import NewMed, Update, NewOrder, PresOrders, DeleteMed, CounterOrder

from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'safety'
api = Api(app)

app.config['JWT_AUTH_URL_RULE'] = '/login'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=99999999999)

jwt = JWT(app, authenticate, identity)  # authentication

api.add_resource(UserRegister, '/sign_up')
api.add_resource(ForgetPassword, '/forget_password')
api.add_resource(CheckUser, '/check_user')
api.add_resource(SetProfile, '/set_profile')
api.add_resource(GetProfile, '/get_profile')
api.add_resource(AllMeds, '/all_meds')
api.add_resource(CatCall, '/cat_call')
api.add_resource(Search, '/search')
api.add_resource(AddOrder, '/add_order')
api.add_resource(DecStock, '/dec_stock')
api.add_resource(ListOrders, '/list_order')
api.add_resource(PresOrder, '/pres_order')


api.add_resource(Orders, '/orders')
api.add_resource(Complete, '/complete')

api.add_resource(Update, '/update')
api.add_resource(NewMed, '/new_med')
api.add_resource(DeleteMed, '/del_med')
api.add_resource(NewOrder, '/new_order')
api.add_resource(PresOrders, '/presorders')
api.add_resource(CounterOrder, '/counter_order')





if __name__ == "__main__":
    app.run(port=5000, debug=True)
