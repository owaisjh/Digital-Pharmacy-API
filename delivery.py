import sqlite3
from flask_restful import Resource, reqparse
import json
import datetime


class Orders(Resource):
 
    def post(self):
        connection = sqlite3.connect('order.db')

        cursor = connection.cursor()
        query = "SELECT * FROM orders WHERE status=0"
        result = cursor.execute(query).fetchall()

        if len(result)==0:
            return {"message": "No Orders"}, 400

        else:
            ll = []
            for i in range(len(result)):
                tp = {
                        "id": result[i][0],
                        "name": result[i][2],
                        "items": result[i][3],
                        "cost": result[i][4],
                        "address": result[i][5],
                        "contact": result[i][6],
                        "payment-type": result[i][7],
                        "date-rec": result[i][9]
                        }
                ll.append(tp)
            final = []
            final.append(len(ll))
            final.append(ll)
            connection.commit()
            connection.close()
            return final, 200



class Complete(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('id',
                        type=int,
                        required=True,
                        help="This field cannot be left blank.")

    def post(self):
        data= Complete.parser.parse_args()
        connection = sqlite3.connect('order.db')
        cursor = connection.cursor()
        query = "UPDATE orders SET datecomp = ? , status = 1 WHERE id = ? "
        lol = (datetime.datetime.now(),data['id'])
        cursor.execute(query, lol)
        connection.commit()
        connection.close()
        return True, 201







