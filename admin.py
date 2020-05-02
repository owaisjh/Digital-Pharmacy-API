import sqlite3
from flask_restful import Resource, reqparse
import json
import datetime
from datetime import date
import sys
from dateutil import relativedelta



class NewMed(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('data',
                        required=True,
                        help="This field cannot be left blank.")

    def post(self):

        data = NewMed.parser.parse_args()
        connection = sqlite3.connect('meds.db')
        cursor = connection.cursor()
        y = json.loads(data["data"])

        '''
         query = "SELECT * FROM allmeds WHERE medname=?"
         result = cursor.execute(query, (data['name'],)).fetchall()

         if result:
             return {"message": "A medicine already exists"}, 400

         '''

        for i in range(y[0]):
            query = "INSERT INTO allmeds VALUES (?, ?, ?, ?)"
            cursor.execute(query, (y[1][i]["name"], y[1][i]["category"], y[1][i]["cost"], y[1][i]["quantity"]))
            create_table = "CREATE TABLE IF NOT EXISTS "+y[1][i]["category"]+" (medname text, cost int, quantity int)"
            cursor.execute(create_table)

            query = "INSERT INTO "+y[1][i]["category"]+" VALUES (?, ?, ?)"
            cursor.execute(query, (y[1][i]["name"], y[1][i]["cost"], y[1][i]["quantity"]))

        connection.commit()
        connection.close()

        return True, 201

class Update(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('data',
                        required=True,
                        help="This field cannot be left blank.")


    def post(self):
        data= Update.parser.parse_args()
        y = json.loads(data["data"])

        connection = sqlite3.connect('meds.db')
        cursor = connection.cursor()


        for i in range(y[0]):
            query = "SELECT * FROM allmeds WHERE medname=?"
            result = cursor.execute(query, (y[1][i]["name"],)).fetchone()

            query = "UPDATE allmeds SET cost = ? , quantity = ? WHERE medname = ?"
            lol = (y[1][i]['cost'], result[3]+y[1][i]['quantity'], y[1][i]['name'])
            cursor.execute(query, lol)

            query = "UPDATE "+y[1][i]['category']+" SET cost = ? , quantity = ? WHERE medname = ?"
            lol = (y[1][i]['cost'], result[3] + y[1][i]['quantity'], y[1][i]['name'])
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
        #for i in range(len(result)):
        tp = {
                    "id": result[0][0],
                    "username": result[0][1],
                    "pres": result[0][2],
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

    parser.add_argument('data',
                        type=str,
                        required=True,
                        help="This field cannot be left blank.")

    def post(self):
        data = NewOrder.parser.parse_args()
        y = json.loads(data["data"])
        connection = sqlite3.connect('meds.db')
        cursor = connection.cursor()

        order = ""
        cost = 0
        for i in range(y[0]):
            query = "SELECT * FROM allmeds WHERE medname=?"
            result = cursor.execute(query, (y[1][i]["name"],)).fetchone()
            if not (result[3] - y[1][i]["quantity"] >= 0):
                return False, 400

        connection.commit()
        connection.close()


        connection = sqlite3.connect('order.db')
        cursor = connection.cursor()
        query = "UPDATE presorder SET status = 1 WHERE id = ? "
        lol = (data['id'],)
        cursor.execute(query, lol)

        connection.commit()
        connection.close()

        connection = sqlite3.connect('meds.db')
        cursor = connection.cursor()
        for i in range(y[0]):

            query = "SELECT * FROM allmeds WHERE medname=?"
            result = cursor.execute(query, (y[1][i]["name"],)).fetchone()



            query = "UPDATE allmeds SET quantity = ? WHERE medname = ?"
            cursor.execute(query, (result[3] - y[1][i]["quantity"], y[1][i]["name"]))

            query = "UPDATE " + result[1] + " SET quantity = ? WHERE medname = ?"
            cursor.execute(query, (result[3] - y[1][i]["quantity"], y[1][i]["name"]))

            cost = cost + (result[2] * y[1][i]["quantity"])

            if (y[1][i]["quantity"] != 0):
                for j in range(y[1][i]["quantity"]):
                    order = order + y[1][i]["name"] + "||"




        connection.commit()
        connection.close()


        if (len(order) != 0):
            connection = sqlite3.connect('user.db')
            cursor = connection.cursor()
            query = "SELECT * FROM users WHERE username=?"
            result = cursor.execute(query, (data['username'],)).fetchone()
            connection.commit()
            connection.close()

            connection = sqlite3.connect('order.db')
            cursor = connection.cursor()
            query = "INSERT INTO orders VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, 0, ?, NULL)"
            cursor.execute(query, (data['username'], result[3], order, cost, result[4], result[5], "Cash on Delivery", datetime.datetime.now()))

            query = "UPDATE presorder SET status = 1 WHERE id = ? "
            lol = (data['id'],)
            cursor.execute(query, lol)

            connection.commit()
            connection.close()

            return True, 200

        else:
            return False, 400



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
            if not (result[3] - y[1][i]["quantity"] >= 0):
                return False, 400


        for i in range(y[0]):

            query = "SELECT * FROM allmeds WHERE medname=?"
            result = cursor.execute(query, (y[1][i]["name"],)).fetchone()

            query = "UPDATE allmeds SET quantity = ? WHERE medname = ?"
            cursor.execute(query, (result[3] - y[1][i]["quantity"], y[1][i]["name"]))

            query = "UPDATE " + result[1] + " SET quantity = ? WHERE medname = ?"
            cursor.execute(query, (result[3] - y[1][i]["quantity"], y[1][i]["name"]))

            cost = cost + (result[2] * y[1][i]["quantity"])

            if (y[1][i]["quantity"] != 0):
                for j in range(y[1][i]["quantity"]):
                    order = order + y[1][i]["name"] + "||"

        connection.commit()
        connection.close()

        if(len(order)!=0):
            connection = sqlite3.connect('order.db')
            cursor = connection.cursor()
            query = "INSERT INTO orders VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, 1, ?, ?)"
            cursor.execute(query, ("Counter-Order", "Counter-Order", order, cost, "Counter-Order", 0, data['payment-type'], datetime.datetime.now(), datetime.datetime.now()))
            connection.commit()
            connection.close()
            return True, 200

        else:
            return False, 400



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
        data= DeleteMed.parser.parse_args()

        connection = sqlite3.connect('meds.db')

        cursor = connection.cursor()

        query = "DELETE FROM allmeds WHERE medname=?"
        cursor.execute(query, (data['name'],))

        query = "DELETE FROM " + data["category"] + " WHERE medname=?"
        cursor.execute(query, (data['name'],))

        connection.commit()
        connection.close()

        return True, 200

class FrontPage(Resource):
    def post(self):
        connection = sqlite3.connect('order.db')
        cursor = connection.cursor()




        currentMonth = datetime.datetime.today().month
        currentYear = datetime.datetime.today().year

        if currentMonth < 10:
            startdate = str(currentYear) + "-0" + str(currentMonth) + "-01"
        else:
            startdate = str(currentYear) + "-" + str(currentMonth) + "-01"

        query = "SELECT SUM(cost) FROM orders WHERE daterec >='" + startdate + " 00:00:00.000' AND daterec <= '" + str(datetime.date.today() + datetime.timedelta(days=1)) + "'"
        result = cursor.execute(query).fetchone()
        month = result[0]
        if month == None:
            month = 0




        query = "SELECT COUNT(cost) FROM orders WHERE username = 'Counter-Order' AND  daterec >= '" + str(date.today()) + " 00:00:00.000' AND daterec <= '" + str(datetime.date.today() + datetime.timedelta(days=1)) + "'"
        result = cursor.execute(query).fetchone()
        counterorder = result[0]
        if counterorder == None:
            counterorder = 0





        query = "SELECT COUNT(cost) FROM orders WHERE username != 'Counter-Order' AND  daterec >= '" + str(date.today()) + " 00:00:00.000' AND daterec <= '" + str(datetime.date.today() + datetime.timedelta(days=1)) + "'"
        result = cursor.execute(query).fetchone()
        apporder = result[0]
        if apporder == None:
            apporder = 0





        startdate = str(currentYear) + "-01-01"

        query = "SELECT SUM(cost) FROM orders WHERE daterec >='" + startdate + " 00:00:00.000' AND daterec <= '" + str(datetime.date.today() + datetime.timedelta(days=1)) + "'"
        result = cursor.execute(query).fetchone()
        year = result[0]
        if year == None:
            year = 0





        currentYear = datetime.datetime.today().year
        currentMonth = datetime.datetime.today().month

        if currentMonth < 10:
            startdate = str(currentYear) + "-0" + str(currentMonth) + "-01"
        else:
            startdate = str(currentYear) + "-" + str(currentMonth) + "-01"

        eightmonths=[]

        query = "SELECT SUM(cost) FROM orders WHERE daterec >='" + startdate + " 00:00:00.000' AND daterec <= '" + str(datetime.date.today() + datetime.timedelta(days=1)) + "'"
        result = cursor.execute(query).fetchone()
        lol = 0
        if result[0] == None:
            lol = 0
        else:
            lol = result[0]

        temp={"startdate": startdate, "total": lol}
        eightmonths.append(temp)


        dates=[]
        today = datetime.date.today()
        startdate = today.replace(day=1)
        dates.append(str(startdate))

        for i in range(7):
            startdate=startdate + relativedelta.relativedelta(months=-1)
            dates.append(str(startdate))


        i=0
        while i<7:
            query = "SELECT SUM(cost) FROM orders WHERE daterec >='" + dates[i+1] + " 00:00:00.000' AND daterec <= '" + dates[i] + " 00:00:00.000'"
            result = cursor.execute(query).fetchone()
            lol = 0
            if result[0] == None:
                lol = 0
            else:
                lol = result[0]

            temp = {"startdate": dates[i+1], "total": lol}
            eightmonths.append(temp)
            i=i+1















        if currentMonth < 10:
            startdate = str(currentYear) + "-0" + str(currentMonth) + "-01"
        else:
            startdate = str(currentYear) + "-" + str(currentMonth) + "-01"

        query = "SELECT * FROM orders WHERE daterec >='" + startdate + " 00:00:00.000' AND daterec <= '" + str(
            datetime.date.today() + datetime.timedelta(days=1)) + "'"
        result = cursor.execute(query).fetchall()
        connection.commit()
        connection.close()

        #code for top 3
        def getcat(name):
            connection = sqlite3.connect('meds.db')
            cursor = connection.cursor()
            query = "SELECT * FROM allmeds WHERE medname= '"+name+"'"
            result = cursor.execute(query).fetchone()
            connection.commit()
            connection.close()
            if result!=None:
                return result[1], result[2]
            else:
                return None

        list = []
        def doescatexist(cat):
            for p in range(len(list)):
                if list[p]['category'] == cat:
                    return p
            return None

        items=[]
        for i in range(len(result)):
            j=0
            save=0
            while j< len(result[i][3]):
                if (result[i][3][j] == '|'):
                    items.append(result[i][3][save:j])
                    save=j+2
                    j=j+1
                    if j+1 == len(result[i][3]):
                        break
                j= j+1


        for i in items:
            cat,cost = getcat(i)
            pos= doescatexist(cat)
            if pos!= None:
                list[pos]["total"]= list[pos]["total"] + cost
            else:
                temp= {"category": cat, "total": cost}
                list.append(temp)



        third = first = second = {"category": "-", "total": -sys.maxsize}

        for i in range(len(list)):
            if (list[i]["total"] > first["total"]):

                    third = second
                    second = first
                    first = list[i]

            elif (list[i]["total"] > second["total"]):

                    third = second
                    second = list[i]

            elif (list[i]["total"] > third["total"]):
                third = list[i]

        top3=[]
        top3.append(first)
        top3.append(second)
        top3.append(third)






        response = {    "month": month,
                        "year": year,
                        "counterorder": counterorder,
                        "apporder": apporder,
                        "eightmonths": eightmonths,
                        "topthree": top3,
                        "allbycat": list
                    }

        return response,200




