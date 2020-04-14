import sqlite3
from flask_restful import Resource, reqparse
import json



class NewMed(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank.")

    parser.add_argument('category',
                        type=str,
                        required=True,
                        help="This field cannot be left blank.")

    parser.add_argument('cost',
                        type=int,
                        required=True,
                        help="This field cannot be left blank.")

    parser.add_argument('quantity',
                        type=int,
                        required=True,
                        help="This field cannot be left blank.")


    def post(self):

        data = NewMed.parser.parse_args()
        connection = sqlite3.connect('meds.db')

        cursor = connection.cursor()
        query = "SELECT * FROM allmeds WHERE medname=?"
        result = cursor.execute(query, (data['name'],)).fetchall()

        if result:
            return {"message": "A medicine already exists"}, 400

        else:
            query = "INSERT INTO allmeds VALUES (?, ?, ?, ?)"
            cursor.execute(query, (data["name"], data["category"], data["cost"], data["quantity"]))
            create_table = "CREATE TABLE IF NOT EXISTS "+data["category"]+" (medname text, cost int, quantity int)"
            cursor.execute(create_table)

            query = "INSERT INTO "+data["category"]+" VALUES (?, ?, ?)"
            cursor.execute(query, (data["name"], data["cost"], data["quantity"]))
        connection.commit()
        connection.close()

        return True, 201

class Update(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank.")

    parser.add_argument('category',
                        type=str,
                        required=True,
                        help="This field cannot be left blank.")

    parser.add_argument('cost',
                        type=int,
                        required=True,
                        help="This field cannot be left blank.")

    parser.add_argument('quantity',
                        type=int,
                        required=True,
                        help="This field cannot be left blank.")

    def post(self):
        data= Update.parser.parse_args()

        connection = sqlite3.connect('meds.db')
        cursor = connection.cursor()

        query = "SELECT * FROM allmeds WHERE medname=?"
        result = cursor.execute(query, (data['name'],)).fetchall()


        if len(result) == 0:
            return {"message": "Please Add The Medicine First"}, 400

        query = "UPDATE allmeds SET cost = ? , quantity = ? WHERE medname = ?"
        lol = (data['cost'], data['quantity'], data['name'])
        cursor.execute(query, lol)

        query = "UPDATE "+data['category']+" SET cost = ? , quantity = ? WHERE medname = ?"
        lol = (data['cost'], data['quantity'], data['name'])
        cursor.execute(query, lol)

        connection.commit()
        connection.close()

        return True, 201

class PresOrders(Resource):
    def post(self):

        connection = sqlite3.connect('order.db')
        cursor = connection.cursor()

        query = "SELECT * FROM presorder WHERE status = 0"
        result = cursor.execute(query).fetchall()

        ll = []
        for i in range(len(result)):
            tp = {
                "id": result[i][0],
                "username": result[i][1],
                "pres": result[i][2],
            }
            ll.append(tp)

        final = []
        final.append(len(ll))
        final.append(ll)
        return final, 200

class NewOrder(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id',
                        type=str,
                        required=True,
                        help="This field cannot be left blank.")

    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank.")

    parser.add_argument('items',
                        type=str,
                        required=True,
                        help="This field cannot be left blank.")

    parser.add_argument('cost',
                        type=int,
                        required=True,
                        help="This field cannot be left blank.")


    def post(self):
        data = NewOrder.parser.parse_args()
        connection = sqlite3.connect('user.db')
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (data['username'],)).fetchone()
        connection.commit()
        connection.close()

        connection = sqlite3.connect('order.db')
        cursor = connection.cursor()
        query = "INSERT INTO orders VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, 0)"
        cursor.execute(query, (data['username'], result[3], data['items'], data['cost'], result[4], result[5], "Cash on Delivery"))

        query = "UPDATE presorder SET status = 1 WHERE id = ? "
        lol = (data['id'],)
        cursor.execute(query, lol)

        connection.commit()
        connection.close()

        return True, 200


class CounterOrder(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('data',
                        required=True,
                        help="This field cannot be left blank.")

    parser.add_argument('payment-type',
                        type=str,
                        required=True,
                        help="This field cannot be left blank.")

    def post(self):
        data = CounterOrder.parser.parse_args()

        y = json.loads(data["data"])
        connection = sqlite3.connect('meds.db')
        cursor = connection.cursor()

        order =""
        cost = 0


        for i in range(y[0]):

            query = "SELECT * FROM allmeds WHERE medname=?"
            result = cursor.execute(query, (y[1][i]["name"],)).fetchone()


            if (result[3] - y[1][i]["quantity"] >= 0):

                query = "UPDATE allmeds SET quantity = ? WHERE medname = ?"
                cursor.execute(query, (result[3] - y[1][i]["quantity"], y[1][i]["name"]))

                query = "UPDATE " + result[1] + " SET quantity = ? WHERE medname = ?"
                cursor.execute(query, (result[3] - y[1][i]["quantity"], y[1][i]["name"]))

                cost = cost + (result[2] * y[1][i]["quantity"])

                if (y[1][i]["quantity"] != 0):
                    for j in range(y[1][i]["quantity"]):
                        order = order + y[1][i]["name"] + "||"

            else:
                connection.commit()
                connection.close()
                return False, 400



        connection.commit()
        connection.close()

        if(len(order)!=0):
            connection = sqlite3.connect('order.db')
            cursor = connection.cursor()
            query = "INSERT INTO orders VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, 1)"
            cursor.execute(query, ("Counter-Order", "Counter-Order", order, cost, "Counter-Order", 0, data['payment-type']))
            connection.commit()
            connection.close()

        return True, 200




class DeleteMed(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank.")

    parser.add_argument('category',
                        type=str,
                        required=True,
                        help="This field cannot be left blank.")

    def post(self):
        data = DeleteMed.parser.parse_args()
        connection = sqlite3.connect('meds.db')

        cursor = connection.cursor()

        query = "DELETE FROM allmeds WHERE medname=?"
        cursor.execute(query, (data['name'],))


        query = "DELETE FROM "+data["category"]+" WHERE medname=?"
        cursor.execute(query, (data['name'],))

        connection.commit()
        connection.close()

        return True, 200

