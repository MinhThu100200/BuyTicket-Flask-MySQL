from datetime import date, timedelta

import pymysql
from pychartjs import BaseChart, ChartType, Color
from sqlalchemy import func

from mainapp.models import *
from flask import render_template, redirect, request, jsonify, session
import hashlib
import json
import uuid
import hmac
from urllib.request import urlopen, Request

domain = "http://127.0.0.1:8004/"


# region payMomo
def payByMomo(Amount):
    endpoint = "https://test-payment.momo.vn/gw_payment/transactionProcessor"
    partnerCode = "MOMOGQOC20201207"
    accessKey = "tb0AnQrtECJ3H0Zu"
    serectkey = "2l9NSfk8rWqc4CpYGZva7dBfCYo9xM25"
    orderInfo = "Thanh toán vé máy bay "
    returnUrl = domain + "api/paymomo"
    notifyurl = "https://dummy.url/notify"
    amount = Amount
    orderId = str(uuid.uuid4())
    requestId = str(uuid.uuid4())
    requestType = "captureMoMoWallet"
    extraData = "merchantName=;merchantId="  # pass empty value if your merchant does not have stores else merchantName=[storeName]; merchantId=[storeId] to identify a transaction map with a physical store
    # before sign HMAC SHA256 with format
    # partnerCode=$partnerCode&accessKey=$accessKey&requestId=$requestId&amount=$amount&orderId=$oderId&orderInfo=$orderInfo&returnUrl=$returnUrl&notifyUrl=$notifyUrl&extraData=$extraData
    rawSignature = "partnerCode=" + partnerCode + "&accessKey=" + accessKey + "&requestId=" + requestId + "&amount=" + amount + "&orderId=" + orderId + "&orderInfo=" + orderInfo + "&returnUrl=" + returnUrl + "&notifyUrl=" + notifyurl + "&extraData=" + extraData
    h = hmac.new(bytes(serectkey, 'utf-8'), rawSignature.encode('utf8'), hashlib.sha256)
    signature = h.hexdigest()
    data = {
        'partnerCode': partnerCode,
        'accessKey': accessKey,
        'requestId': requestId,
        'amount': amount,
        'orderId': orderId,
        'orderInfo': orderInfo,
        'returnUrl': returnUrl,
        'notifyUrl': notifyurl,
        'extraData': extraData,
        'requestType': requestType,
        'signature': signature
    }
    data = json.dumps(data).encode('utf-8')
    clen = len(data)
    req = Request(endpoint, data, {'Content-Type': 'application/json', 'Content-Length': clen})
    f = urlopen(req)
    response = f.read()
    f.close()
    return json.loads(response)['payUrl']


# endregion


def query(id):
    if (id == "1"):
        return " Select Year(datetime_bill) as 'Nam', Sum(money) as 'Doanh thu' From saledb.bill Group by Year(datetime_bill)  order by Year(datetime_bill) asc"
    elif (id == "2"):
        return "SELECT DATE_FORMAT(datetime_bill, '%d-%m') , SUM(money) AS DOANHTHU  FROM saledb.bill where month(datetime_bill)>=1 and month(datetime_bill)<=3 and year(datetime_bill)=year(current_date()) GROUP BY DATE_FORMAT(datetime_bill, '%d-%m') ORDER BY datetime_bill ASC"
    elif (id == "3"):
        return "SELECT DATE_FORMAT(datetime_bill, '%d-%m') , SUM(money) AS DOANHTHU  FROM saledb.bill where month(datetime_bill)>=4 and month(datetime_bill)<=6 and year(datetime_bill)=year(current_date()) GROUP BY DATE_FORMAT(datetime_bill, '%d-%m') ORDER BY datetime_bill ASC"
    elif (id == "4"):
        return "SELECT DATE_FORMAT(datetime_bill, '%d-%m') , SUM(money) AS DOANHTHU  FROM saledb.bill where month(datetime_bill)>= 7 and month(datetime_bill)<=9 and year(datetime_bill)=year(current_date()) GROUP BY DATE_FORMAT(datetime_bill, '%d-%m') ORDER BY datetime_bill ASC"
    elif (id == "5"):
        return "SELECT DATE_FORMAT(datetime_bill, '%d-%m') , SUM(money) AS DOANHTHU  FROM saledb.bill where month(datetime_bill)>=10 and month(datetime_bill)<=12 and year(datetime_bill)=year(current_date()) GROUP BY DATE_FORMAT(datetime_bill, '%d-%m') ORDER BY datetime_bill ASC"
    elif (id == "6"):
        return "SELECT DATE_FORMAT(datetime_bill,'%m') as 'Tháng' , SUM(money) AS DOANHTHU FROM saledb.bill where month(datetime_bill)>=1 and month(datetime_bill)<=12 and year(datetime_bill)=year(current_date()) GROUP BY DATE_FORMAT(datetime_bill, '%m') ORDER BY datetime_bill ASC"


def get_data_label(query):
    labels = []
    data = []
    connection = pymysql.connect('localhost', 'root', '12345678', 'saledb')
    try:
        with connection.cursor() as cursor:
            sql = query
            cursor.execute(sql)
            x = cursor.fetchall()
            for item in x:
                labels.append(str(item[0]))
                data.append(str(item[1]))
    finally:
        connection.close()
    return labels, data


class MyBarGraphYears(BaseChart):
    type = ChartType.Line

    class labels:
        group = get_data_label(query("1")).__getitem__(0)

    class data:
        # label = labels
        data = get_data_label(query("1")).__getitem__(1)
        # backgroundColor = Color.Palette(Color.Hex('#5AC18E'), 12, 'lightness')
        borderColor = Color.Magenta
        backgroundColor = Color.Transparent

    class options:
        title = {"text": "DOANH THU QUA CÁC NĂM ", "display": True}
        scales = {
            "yAxes": [
                {
                    "ticks": {
                        "beginAtZero": True,
                    }
                }
            ]
        }


class MyBarGraphQ1(BaseChart):
    type = ChartType.Line

    class labels:
        group = get_data_label(query("2")).__getitem__(0)

    class data:
        # label = labels
        data = get_data_label(query("2")).__getitem__(1)
        # backgroundColor = Color.Palette(Color.Hex('#5AC18E'), 12, 'lightness')
        borderColor = Color.Blue
        backgroundColor = Color.Beige

    class options:
        title = {"text": "DOANH THU THEO QUÝ 1", "display": True}
        scales = {
            "yAxes": [
                {
                    "ticks": {
                        "beginAtZero": True,
                    }
                }
            ]
        }


class MyBarGraphQ2(BaseChart):
    type = ChartType.Line

    class labels:
        group = get_data_label(query("3")).__getitem__(0)

    class data:
        # label = labels
        data = get_data_label(query("3")).__getitem__(1)
        # backgroundColor = Color.Palette(Color.Hex('#5AC18E'), 12, 'lightness')
        borderColor = Color.Blue
        backgroundColor = Color.Beige

    class options:
        title = {"text": "DOANH THU THEO QUÝ 2", "display": True}
        scales = {
            "yAxes": [
                {
                    "ticks": {
                        "beginAtZero": True,
                    }
                }
            ]
        }


class MyBarGraphQ3(BaseChart):
    type = ChartType.Line

    class labels:
        group = get_data_label(query("4")).__getitem__(0)

    class data:
        # label = labels
        data = get_data_label(query("4")).__getitem__(1)
        # backgroundColor = Color.Palette(Color.Hex('#5AC18E'), 12, 'lightness')
        borderColor = Color.Blue
        backgroundColor = Color.Beige

    class options:
        title = {"text": "DOANH THU THEO QUÝ 3", "display": True}
        scales = {
            "yAxes": [
                {
                    "ticks": {
                        "beginAtZero": True,
                    }
                }
            ]
        }


class MyBarGraphQ4(BaseChart):
    type = ChartType.Line

    class labels:
        group = get_data_label(query("5")).__getitem__(0)

    class data:
        # label = labels
        data = get_data_label(query("5")).__getitem__(1)
        # backgroundColor = Color.Palette(Color.Hex('#5AC18E'), 12, 'lightness')
        borderColor = Color.Blue
        backgroundColor = Color.Beige

    class options:
        title = {"text": "DOANH THU THEO QUÝ 4", "display": True}
        scales = {
            "yAxes": [
                {
                    "ticks": {
                        "beginAtZero": True,
                    }
                }
            ]
        }


class MyBarGraphByMonths(BaseChart):
    type = ChartType.Bar

    class labels:
        group = get_data_label(query("6")).__getitem__(0)

    class data:
        # label = labels
        data = get_data_label(query("6")).__getitem__(1)
        # backgroundColor = Color.Palette(Color.Hex('#5AC18E'), 12, 'lightness')
        borderColor = Color.Blue
        backgroundColor = Color.Beige

    class options:
        title = {"text": "DOANH THU THEO TỪNG THÁNG TRONG NĂM", "display": True}
        scales = {
            "yAxes": [
                {
                    "ticks": {
                        "beginAtZero": True,
                    }
                }
            ]
        }


def draw_chart(type):
    if (type == "1"):
        NewChart = MyBarGraphYears()
        NewChart.data.label = "Doanh Thu"
    if (type == "2"):
        NewChart = MyBarGraphQ1()
        NewChart.data.label = "Doanh Thu"
    if (type == "3"):
        NewChart = MyBarGraphQ2()
        NewChart.data.label = "Doanh Thu"
    if (type == "4"):
        NewChart = MyBarGraphQ3()
        NewChart.data.label = "Doanh Thu"
    if (type == "5"):
        NewChart = MyBarGraphQ4()
        NewChart.data.label = "Doanh Thu"
    if (type == "6"):
        NewChart = MyBarGraphByMonths()
        NewChart.data.label = "Doanh Thu"
    ChartJSON = NewChart.get()
    return ChartJSON


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
        return (name, username, password, phone, email)

    return None


def get_id(query, val):
    data = 0

    connection = pymysql.connect('localhost', 'root', 'tan240600', 'saledb')

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
    val = id

    list_name = read_data_para(query, val)

    for i in list_name:
        name_air.append(i[0])

    return name_air


def all_flight():
    list_flight = []

    l1 = Flight.query.join(FlightRoute). \
        add_columns(Flight.id, Flight.time_begin, Flight.time_end, Flight.date_flight_from, FlightRoute.name,
                    Flight.date_flight_to, FlightRoute.id_airport1,
                    FlightRoute.id_airport2, Flight.plane_id). \
        filter(Flight.flight_route_id == FlightRoute.id).all()

    l2 = Flight.query.join(Plane). \
        add_columns(Flight.id, Plane.quantity, Plane.amount_of_seat1, Plane.amount_of_seat2). \
        filter(Flight.plane_id == Plane.id).all()
    d = Rule3.query.all()
    for i in d:
        amount = i.amount
    for i in l1:
        if i.date_flight_from >= date.today() + timedelta(amount):
            for num in l2:
                if num.id == i.id:
                    name1 = Airport.query.add_columns(Airport.name).filter(i.id_airport1 == Airport.id).one()
                    name2 = Airport.query.add_columns(Airport.name).filter(i.id_airport2 == Airport.id).one()
                    booked = db.session.query(func.sum(Booking.amount_seat)).filter(i.id == Booking.flight_id).scalar()
                    if booked == None:
                        booked = 0
                    empty = num.quantity - booked
                    if empty == 0:
                        pass
                    dic = {
                        'id': i.id,
                        'name': i.name,
                        'name1': name1,
                        'name2': name2,
                        'flight_name': i.name,
                        'date_from': i.date_flight_from,
                        'time_begin': i.time_begin,
                        'date_end': i.date_flight_to,
                        'time_end': i.time_end,
                        'seat1': num.amount_of_seat1,
                        'seat2': num.amount_of_seat2,
                        'empty': num.quantity - booked,
                        'booked': booked,
                    }

            list_flight.append(dic)

    return (list_flight)


def add_client(name, phone, idcard):
    query = "SELECT * FROM client"
    clients = read_data(query)

    id = len(clients) + 1
    name = name.strip()
    phone = phone.strip()
    idcard = idcard.strip()

    query_add = "INSERT INTO client (id,name,phone,idcard) VALUES (%s,%s,%s,%s)"
    val = (id, name, phone, idcard)
    sign = add_data(query_add, val)

    if sign == 1:
        return (val)

    return None


def cart_stats(cart):
    count = 0
    price = 0
    if cart:
        for p in cart.values():
            count = count + p['quantity']
            price = price + p['quantity'] * p['price']
        return count, price


def add_airport(name):
    query = "SELECT * FROM airport"
    airports = read_data(query)
    air = Airport.query.all()
    id = len(airports) + 1
    name = name.strip()
    for a in air:
        if name == a.name:
            return None
    query_add = "INSERT INTO airport (id,name) VALUES (%s,%s)"
    val = (id, name)
    sign = add_data(query_add, val)

    if sign == 1:
        return (val)
    return None


def add_total(cart, client):
    user = session['user']
    total_quantity, total_amount = cart_stats(session.get('cart'))
    card = []
    for p in list(cart.values()):
        flag = 0
        price_flight_id = PriceFlight.query.add_columns(PriceFlight.id).filter(
            PriceFlight.vnd == p['price'] and PriceFlight.flight_id == p['id']).first()
        price_flight_name = PriceFlight.query.add_columns(PriceFlight.name).filter(
            PriceFlight.vnd == p['price'] and PriceFlight.flight_id == p['id']).first()

        if '1' in price_flight_name[1]:
            for c in list(client.values()):
                if int(c['id_flight_now']) == int(p['id']) and int(c['price']) == p['price']:
                    for i in card:
                        if c['id_card'] == i:
                            flag = 1
                if flag == 0:
                    card.append(c['id_card'])
                    print(type(price_flight_id[1]))
                    print(type(p['id']))
                    print(type(c['id']))
                    print(type(user[0]))

                    ticket = add_ticket(price_flight_id[1], 1, p['id'], c['id'], user[0])
                    print(ticket)

        else:
            for c in list(client.values()):
                if c['id_flight_now'] == str(p['id']) and int(c['price']) == p['price']:
                    for i in card:
                        if c['id_card'] == i:
                            flag = 1
                if flag == 0:
                    card.append(c['id_card'])
                    ticket = add_ticket(price_flight_id[1], 2, p['id'], c['id'], user[0])
                    print(ticket)
        for c in list(client.values()):
            print(p['quantity'], c['id'], p['id'])
            booking = add_booking(p['quantity'], c['id'], p['id'])
            print(booking)
            print(p['quantity'], c['id'], p['id'])
            bill = add_bill(total_amount, c['id'], user[0])
            print(bill)
            break


def add_ticket(pf_id, ty_id, f_id, client_id, user_id):
    query = "SELECT * FROM ticket"
    tickets = read_data(query)

    id = len(tickets) + 1
    price_flight_id = int(pf_id)
    type_id = int(ty_id)
    flight_id = int(f_id)
    client_id = int(client_id)
    user_id = int(user_id)
    query_add = "INSERT INTO ticket (id,status,price_flight_id,type_ticket_id,flight_id,client_id,user_id) VALUES (%s,%s,%s,%s,%s,%s,%s)"
    val = (id, 1, price_flight_id, type_id, flight_id, client_id, user_id)
    sign = add_data(query_add, val)

    if sign == 1:
        return val

    return None


def add_booking(amount_seat, client_id, flight_id):
    query = "SELECT * FROM booking"
    bookings = read_data(query)

    id = len(bookings) + 2
    amount_seat = int(amount_seat)
    datetime_booking = date.today()
    client_id = int(client_id)
    flight_id = int(flight_id)
    query_add = "INSERT INTO booking (id,datetime_booking,amount_seat,client_id,flight_id) VALUES (%s,%s,%s,%s,%s)"
    val = (id, datetime_booking, amount_seat, client_id, flight_id)
    sign = add_data(query_add, val)

    if sign == 1:
        return (val)

    return None


def add_bill(money, client_id, user_id):
    query = "SELECT * FROM bill"
    bills = read_data(query)

    id = len(bills) + 1
    money = int(money)
    datetime_booking = date.today()
    client_id = int(client_id)
    user_id = int(user_id)
    query_add = "INSERT INTO bill (id,datetime_bill,money,client_id,user_id) VALUES (%s,%s,%s,%s,%s)"
    val = (id, datetime_booking, money, client_id, user_id)
    sign = add_data(query_add, val)

    if sign == 1:
        return val

    return None


def revenue_month(month, year):
    list_flight = []

    datefrom = year + '-' + month + '-' + '1'
    dateto = year + '-' + month + '-' + '31'

    l1 = Flight.query.join(FlightRoute). \
        add_columns(Flight.id, Flight.time_begin, Flight.time_end, Flight.date_flight_from, FlightRoute.name,
                    Flight.date_flight_to, FlightRoute.id_airport1,
                    FlightRoute.id_airport2, Flight.plane_id). \
        filter(Flight.flight_route_id == FlightRoute.id).filter(Flight.date_flight_from.between(datefrom, dateto)).all()

    l2 = Flight.query.join(Plane). \
        add_columns(Flight.id, Plane.quantity, Plane.amount_of_seat1, Plane.amount_of_seat2). \
        filter(Flight.plane_id == Plane.id).all()

    for i in l1:
        for num in l2:
            if num.id == i.id:
                booked = db.session.query(func.sum(Booking.amount_seat)).filter(
                    i.id == Booking.flight_id).scalar()

                if booked == None:
                    booked = 0

                dic = {
                    'id': i.id,
                    'name': i.name,
                    'date_from': i.date_flight_from,
                    'time_begin': i.time_begin,
                    'date_end': i.date_flight_to,
                    'time_end': i.time_end,
                    'seat1': num.amount_of_seat1,
                    'seat2': num.amount_of_seat2,
                    'quantity': num.quantity,
                    'empty': num.quantity - booked,
                    'rate': round(booked * 100 / num.quantity, 2),
                    'booked': booked,
                }

        list_flight.append(dic)

    return list_flight


def revenue_year(year):
    list_month = []
    for i in range(1, 13):
        month = str(i)
        list_flight = revenue_month(month, year)
        amount_flight = 0
        revenue = 0
        quantity = 0
        booked = 0
        for p in list_flight:
            amount_flight = amount_flight + 1
            revenue = revenue + p['booked'] * 50000
            quantity = quantity + p['quantity']
            booked = booked + p['booked']
        if quantity == 0:
            dic = {
                'id': 0,
                'amount_flight': 0,
                'revenue': 0,
                'rate': 0
            }
        else:
            dic = {
                'id': i,
                'amount_flight': amount_flight,
                'revenue': revenue,
                'rate': round(booked * 100 / quantity, 2)
            }
        list_month.append(dic)
    print(list_month)
    return list_month


def update_rule3(amount):
    query = 'update rule3 set amount = %s where id = 1'
    val = (amount)
    sign = add_data(query, val)

    if sign == 1:
        return val

    return None
