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

        connection = sqlite3.connect('user.db')
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

        connection = sqlite3.connect('user.db')
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
                    "name": save.user_name,
                    "address": save.address,
                    "contact": save.contact
                    }, 200



class AllMeds(Resource):
    def post(self):
        connection = sqlite3.connect('meds.db')
        cursor = connection.cursor()

        query = "SELECT * FROM allmeds"
        result = cursor.execute(query).fetchall()
        ll=[]
        for i in range(len(result)):
            tp={
                "name": result[i][0],
                "category": result[i][1],
                "cost": result[i][2],
                "quantity": result[i][3]
            }
            ll.append(tp)
        final=[]
        final.append(len(ll))
        final.append(ll)
        return final, 200

class CatCall(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('category',
                        type=str,
                        required=True,
                        help="This field cannot be left blank.")
    def post(self):
        data = CatCall.parser.parse_args()
        connection = sqlite3.connect('meds.db')
        cursor = connection.cursor()
        query = "SELECT * FROM "+data['category']
        result = cursor.execute(query).fetchall()
        ll = []
        for i in range(len(result)):
            tp = {
                "name": result[i][0],
                "cost": result[i][1],
                "quantity": result[i][2]
            }
            ll.append(tp)
        final = []
        final.append(len(ll))
        final.append(ll)
        return final, 200

class Search(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank.")
    def post(self):
        data = Search.parser.parse_args()
        connection = sqlite3.connect('meds.db')
        cursor = connection.cursor()

        query = "SELECT * FROM allmeds WHERE medname LIKE '%" + data['name'] + "%'"
        result = cursor.execute(query).fetchall()

        ll = []
        '''
        for i in range(len(result)):
            if data['name'] in result[i][0]:
                tp = {
                    "name": result[i][0],
                    "category": result[i][1],
                    "cost": result[i][2],
                    "quantity": result[i][3]
                }
                ll.append(tp)
        final = []
        final.append(len(ll))
        final.append(ll)
        '''
        for i in range(len(result)):
            tp = {
                    "name": result[i][0],
                    "category": result[i][1],
                    "cost": result[i][2],
                    "quantity": result[i][3]
                }
            ll.append(tp)


        return ll, 200
        #return final, 200


class AddOrder(Resource):
    parser = reqparse.RequestParser()
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
  #  @jwt_required()
    def post(self):
        data = AddOrder.parser.parse_args()
        connection = sqlite3.connect('user.db')
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (data['username'],)).fetchone()
        connection.commit()
        connection.close()

        connection = sqlite3.connect('order.db')
        cursor = connection.cursor()
        query = "INSERT INTO orders VALUES (NULL, ?, ?, ?, ?, ?, ?, 0)"
        cursor.execute(query, (data['username'], result[3], data['items'], data['cost'], result[4], result[5]))
        connection.commit()
        connection.close()
        return True, 200






class DecStock(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank.")
  #  @jwt_required()
    def post(self):
        data = DecStock.parser.parse_args()
        connection = sqlite3.connect('meds.db')
        cursor = connection.cursor()
        query = "SELECT * FROM allmeds WHERE medname=?"
        result = cursor.execute(query, (data["name"],)).fetchone()

       
        if(result[3]>0):
            query = "UPDATE allmeds SET quantity = ? WHERE medname = ?"
            cursor.execute(query,(result[3]-1, data["name"]))

            query = "UPDATE "+result[1]+" SET quantity = ? WHERE medname = ?"
            cursor.execute(query,(result[3]-1, data["name"]))

        else:
            connection.commit()
            connection.close()
            return False, 400

        connection.commit()
        connection.close()

        return True, 200


class Orders(Resource):
 
    def post(self):
        connection = sqlite3.connect('order.db')

        cursor = connection.cursor()
        query = "SELECT * FROM orders"
        result = cursor.execute(query).fetchall()

        if len(result)==0:
            return {"message": "No Orders"}, 400

        else:
            ll = []
            for i in range(len(result)):
                if result[i][7]==0:
                    tp = {
                        "id": result[i][0],
                        "name": result[i][2],
                        "items": result[i][3],
                        "cost": result[i][4],
                        "address": result[i][5],
                        "contact": result[i][6]
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
        query = "UPDATE orders SET status = 1 WHERE id = ? "
        lol = (data['id'],)
        cursor.execute(query, lol)

        connection.commit()
        connection.close()

        return True, 201


class ListOrders(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank.")
    def post(self):
        data = ListOrders.parser.parse_args()
        connection = sqlite3.connect('order.db')
        cursor = connection.cursor()
        query = "SELECT * FROM orders WHERE username = "+data['username']
        result = cursor.execute(query).fetchall()
        ll = []
        for i in range(len(result)):
            tp = {
                "items": result[i][3],
                "cost": result[i][4],
                "status": result[i][7]
            }
            ll.append(tp)
        final = []
        final.append(len(ll))
        final.append(ll)
        return final, 200




         

