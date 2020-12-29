import pymysql
from pychartjs import BaseChart, ChartType, Color
from mainapp.models import *
from flask import render_template, redirect, request, jsonify
import hashlib
'''def get_data_label():
    labels = []

    connection = pymysql.connect('localhost', 'root', '12345678', 'saledb')
    try:
        with connection.cursor() as cursor:

            sql = "SELECT * FROM revenuemonth"
            cursor.execute(sql)

            x = cursor.fetchall()
            for id in x:
               labels.append(str(id[0]))
    finally:
        connection.close()
    return labels

def get_data_value():

    values = []
    connection = pymysql.connect('localhost', 'root', '12345678', 'saledb')
    try:
        with connection.cursor() as cursor:

            sql = "SELECT * FROM revenuemonth"
            cursor.execute(sql)

            x = cursor.fetchall()
            for value in x:
                values.append(int(value[2]))

    finally:
        connection.close()
    return values
class MyBarGraph(BaseChart):

    type = ChartType.Pie
    class labels:
        group = get_data_label()
    class data:
        #label = labels
        data = get_data_value()
        backgroundColor = Color.Palette(Color.Hex('#5AC18E'), 12, 'lightness')
        borderColor = Color.Olive
def draw_chart():
    NewChart = MyBarGraph()
    NewChart.data.label = "Revenue by Year"
    # can change data after creation
    if NewChart.data.data == []:
        NewChart.data.data = [45, 67, 50, 23, 45, 67, 90, 12, 56, 78, 90, 170]
    ChartJSON = NewChart.get()
    return jsonify(ChartJSON)
'''
def read_data(query):
    connection = pymysql.connect('localhost', 'root', '12345678', 'saledb')
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            x = cursor.fetchall()
    finally:
        connection.close()
    return x
def read_data_para(query, val):
    connection = pymysql.connect('localhost', 'root', '12345678', 'saledb')
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, val)
            x = cursor.fetchall()
    finally:
        connection.close()
    return x
def add_data(query, val):
    connection = pymysql.connect('localhost', 'root', '12345678', 'saledb')
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, val)
            connection.commit()
    except:
        return 0
    finally:
        connection.close()
    return 1
def validate_employee(username, password):

    query = "SELECT * FROM user"
    users = read_data(query)
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    for user in users:

        if user[4].strip() == username.strip() and user[5].strip() == password.strip():
            return user

    return None

def add_employee(name, username, password, phone, email):

    query = "SELECT * FROM user"
    users = read_data(query)

    id = len(users) + 1
    name = name.strip()
    username = username.strip()
    phone = phone.strip()
    email = email.strip()
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    query_add = "INSERT INTO user (id,name,email,phone,username,password) VALUES (%s,%s,%s,%s,%s,%s)"
    val = (id, name, email, phone, username, password)
    sign = add_data(query_add, val)

    if sign == 1:
        return(name,username,password,phone,email)

    return None

def get_id(query, val):

    data = 0

    connection = pymysql.connect('localhost', 'root', '12345678', 'saledb')

    try:
        with connection.cursor() as cursor:
            cursor.execute(query, val)
            x = cursor.fetchall()
            for i in x:
                data = int(i[0])
    finally:
        connection.close()
    return data

def get_data_list_1(query):

    data = []

    connection = pymysql.connect('localhost', 'root', '12345678', 'saledb')
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            x = cursor.fetchall()
            for i in x:
                data.append(str(i[1]))
    finally:
        connection.close()

    return data

def get_data_search(air_from, air_to, dte_from):
    query_id_air1 = 'SELECT id FROM airport WHERE name = %s'
    val1 = (air_from)
    id1 = get_id(query_id_air1, val1)
    query_id_air2 = 'SELECT id FROM airport WHERE name = %s'
    val2 = (air_to)
    id2 = get_id(query_id_air2, val2)
    query = 'CALL proc_search_flight(%s,%s,%s)'
    val = (id1, id2, dte_from)
    list_flight = read_data_para(query, val)
    return list_flight

def get_data_search_date(dte_from):
    query = 'CALL proc_search_flight_date(%s)'
    val = (dte_from)
    list_flight = read_data_para(query, val)
    return list_flight

def get_name(id):
    name_air = []
    query = 'SELECT fun_check_name_airport (%s)'
    val = (id)
    list_name = read_data_para(query, val)
    for i in list_name:
        name_air.append(i[0])
    return name_air

def search(id):
    list_flight = []
    l1 = Flight.query.join(FlightRoute). \
        add_columns(Flight.id, Flight.time_begin, Flight.time_end, Flight.date_flight_from, FlightRoute.id_airport1, FlightRoute.id_airport2,
                    Flight.plane_id). \
        filter(Flight.flight_route_id == FlightRoute.id and Flight.id == id).all()
    l2 = Flight.query.join(Plane). \
        add_columns(Plane.amount_of_seat1, Plane.amount_of_seat2). \
        filter(Flight.plane_id == Plane.id and Flight.id == id).all()
    l = l1 + l2
    print(l)
    for i in l:
        name1 = Airport.query.add_columns(Airport.name).filter(i.id_airport1 == Airport.id).one()
        name2 = Airport.query.add_columns(Airport.name).filter(i.id_airport2 == Airport.id).one()
        dt = FlightDetail.flights
        for n in dt:
            detail = FlightDetail.query.add_columns(FlightDetail.inter_airport, FlightDetail.waiting_time, FlightDetail.note).\
                filter(i.id == dt.id)
        dic = {
            'id': i.id,
            'name1': name1,
            'name2': name2,
            'date-from': i.date_flight_from,
            'time-begin': i.time_begin,
            'date-end': i.date_flight_end,
            'time-end': i.time_end,
            'seat1': i.amount_of_seat1,
            'seat2': i.amount_of_seat2,
            'inter_air': detail.inter_air,
            'wating-time': detail.wating_time,
            'note': detail.note
        }
        list_flight.append(dic)

    return(list_flight)



