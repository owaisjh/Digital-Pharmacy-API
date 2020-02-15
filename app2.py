from flask import Flask, request
from flask_restful import Resource, Api

from admin import NewMed, Up


app = Flask(__name__)

api = Api(app)

api.add_resource(Up, '/update')
api.add_resource(NewMed, '/new_med')


app.run(port=6000, debug=True)



