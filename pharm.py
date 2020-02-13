import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import JWT, jwt_required




class User:
    def __init__(self, _id, username, password,  user_name, address, contact):
        self.id = _id
        self.username = username
        self.password = password
        self.user_name = user_name
        self.address = address
        self.contact = contact



    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('user.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username,))
        row = result.fetchone()
        if row is not None:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('user.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query, (_id,))
        row = result.fetchone()
        if row is not None:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank.")

    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank.")

    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank.")

    parser.add_argument('address',
                        type=str,
                        required=True,
                        help="This field cannot be left blank.")

    parser.add_argument('contact',
                        type=int,
                        required=True,
                        help="This field cannot be left blank.")

    def post(self):

        request_data = UserRegister.parser.parse_args()

        if User.find_by_username(request_data["username"]):
            return {"message": "A user with that username already exists"}, 400

        connection = sqlite3.connect('doctor.db')
        cursor = connection.cursor()
        query = "INSERT INTO users VALUES (NULL, ?, ?, ?, ?, ?)"
        cursor.execute(query, (request_data["username"], request_data["password"], request_data["name"], request_data["address"], request_data["contact"]))

        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (request_data["username"],))
        row = result.fetchone()

        connection.commit()
        connection.close()

        return {"id": row[0]}, 201


class SetProfile(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank.")

    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank.")

    parser.add_argument('address',
                        type=str,
                        required=True,
                        help="This field cannot be left blank.")

    parser.add_argument('contact',
                        type=int,
                        required=True,
                        help="This field cannot be left blank.")

    def post(self):
        data= SetProfile.parser.parse_args()

        connection = sqlite3.connect('doctor.db')
        cursor = connection.cursor()
        query = "UPDATE users SET user_name = ? , address = ? , contact = ? WHERE username = ?"
        lol = (data['name'], data['address'], data['contact'], data['username'])
        cursor.execute(query, lol)

        connection.commit()
        connection.close()

        return True, 201


class GetProfile(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank.")
    def post(self):
        data = GetProfile.parser.parse_args()
        save = User.find_by_username(data['username'])

        if save is None:
            return {"message": "username invalid"}, 404
        else:
            return {"id": save.id,
                    "user_name": save.user_name,
                    "address": save.address,
                    "contact": save.contact
                    }, 200



class Test(Resource):
    def post(self):
        connection = sqlite3.connect('meds.db')
        cursor = connection.cursor()

        query = "SELECT * FROM allmeds"
        result = cursor.execute(query).fetchall()
        ll=[]
        for i in range(len(result)):
            tp={
                "id": result[i][0],
                "name": result[i][1],
                "cost": result[i][2],
                "quantity": result[i][3]
            }
            ll.append(tp)
        final=[]
        final.append(len(ll))
        final.append(ll)
        return final, 200


