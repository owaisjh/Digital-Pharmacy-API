from flask import Flask, request
from flask_restful import Resource, Api

from admin import NewMed, Update


app = Flask(__name__)

api = Api(app)

api.add_resource(Update, '/update')
api.add_resource(NewMed, '/new_med')


app.run(port=6000, debug=True)



