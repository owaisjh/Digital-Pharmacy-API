import sqlite3
from flask_restful import Resource, reqparse




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


