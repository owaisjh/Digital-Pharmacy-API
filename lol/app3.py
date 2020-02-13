from flask import Flask, request
from flask_restful import Resource, Api

from delivery import Orders, Complete


app = Flask(__name__)

api = Api(app)

api.add_resource(Orders, '/orders')
api.add_resource(Complete, '/complete')


app.run(port=6000, debug=True)



