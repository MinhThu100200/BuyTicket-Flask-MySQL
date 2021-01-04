import json
from datetime import date
from flask import render_template, redirect, session, request, jsonify, url_for
from mainapp import app, login, dao
from flask_login import login_user
import hashlib
from functools import wraps
from mainapp.models import *

def login_required(f):
    @wraps(f)
    def check(*args, **kwargs):
        if not session.get("user"):
            return redirect(url_for("login", next=request.url))
        return f(*args, **kwargs)
    return check
@app.route("/")
def main():
    return render_template('index.html')

@app.route("/login-admin", methods=['GET', 'POST'])
def login_admin():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password", "")
        password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
        user = User.query.filter(User.username == username.strip(),
                          User.password == password).first()

    if user.type == 1:
        if user:
            login_user(user=user)
        return redirect("/admin")

@login.user_loader
def user_load(user_id):
    return User.query.get(user_id)

@app.route("/employee/login", methods=["GET","POST"])
def login(): #login_user

    err_msg = ""
    
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password", "")
        user = dao.validate_employee(username=username, password=password)

        if user:
            session['user'] = user
            if "next" in request.args:
                return redirect(request.args["next"])
            return redirect('/')
        else:
            err_msg = "Dang nhap khong thanh cong"

    return render_template("employee/login.html", err_msg=err_msg)

@app.route('/logout')
def logout(): #logout user
    session["user"] = None
    return redirect('/')

@app.route('/search',methods=["GET","POST"])
@login_required
def search(): #search chuyen bay
    query = 'SELECT * FROM airport'

    airport = dao.get_data_list_1(query)

    if request.method == 'POST':
        air_from = request.form.get('from')
        air_to = request.form.get('to')
        dte_from = request.form.get('dtefrom')

        if dte_from:
            list_flight = get_data_search(air_from, air_to, dte_from)
            data = {
                'from': air_from,
                'to': air_to,
                'date': dte_from,
            }
            return render_template('search.html', airport=airport, data=data, list_flight=list_flight, len=len(list_flight))
        else:
            dte_from = date.today()
            list_flight = get_data_search(air_from, air_to, dte_from)
            data = {
                'from': air_from,
                'to': air_to,
                'date': dte_from,
            }
            return render_template('search.html', airport=airport, data=data, list_flight=list_flight, len=len(list_flight))

    return render_template('search.html', airport=airport)

@app.route('/api/detail',methods=["GET","POST"])
def add_flight():

    if 'detail' not in session:
        session['detail'] = {}
    detail = session['detail']
    data = request.json
    print(data)
    id = str(data.get('id'))

    detail = {
        'id': id

    }
    session['detail'] = detail
    print(detail)
    return jsonify({'n': detail,
                    'name': 1
                    })

@app.route('/manage-flight',methods=["GET","POST"])
def flight(): #tat ca chuyen bay ngay hom nay

    list_flight = dao.all_flight()
    return render_template('manage-flight.html', list_flight=list_flight)

@app.route('/schedule',methods=["GET","POST"])
def schedule():
    list_detail = []
    f = {}

    flights = dao.all_flight()

    detail = session['detail']
    #print(flights)

    for i in flights:
        #print(i['id'])
        if i['id'] == int(detail['id']):
            dt = FlightDetail.query.add_columns(FlightDetail.inter_airport, FlightDetail.waiting_time, FlightDetail.note). \
                                    filter(FlightDetail.flights.any(id=i['id'])).all()
            f = i
  

    for d in dt:
        dic = {
            'inter_airport': d.inter_airport,
            'waiting_time': d.waiting_time,
            'note': d.note
        }

        list_detail.append(dic)
    #print(f, list_detail)
    return render_template('schedule.html', f=f, list_detail=list_detail)

@app.route('/ticket-flight', methods=['GET', 'POST'])
def ticket_flight():
    clients = Client.query.all()
    price_flight = PriceFlight.query.all()
    price_list = []
    list_detail = []
    f = {}

    flights = dao.all_flight()

    detail = session['detail']
    # print(flights)

    for i in flights:
        # print(i['id'])
        if i['id'] == int(detail['id']):
            dt = FlightDetail.query.add_columns(FlightDetail.inter_airport, FlightDetail.waiting_time,
                                                FlightDetail.note). \
                filter(FlightDetail.flights.any(id=i['id'])).all()
            f = i
    for p in price_flight:
        if p.flight_id == int(detail['id']):
            price_list.append(p)
    for d in dt:
        dic = {
            'inter_airport': d.inter_airport,
            'waiting_time': d.waiting_time,
            'note': d.note
        }

        list_detail.append(dic)
    client_list = []
    for c in clients:
        dic = {
            'id': c.id,
            'name': c.name,
            'phone': c.phone,
            'id_card': c.idcard
        }
        client_list.append(dic)
    id = 0
    if request.method == 'POST':
        id_card = request.form.get('PassengerCMND')
        name = request.form.get('NamePassenger')
        phone = request.form.get('PhonePassenger')
        price = request.form.get('price')
        #quantity = 0
        for c in clients:
            if id_card == c.idcard:
                id = c.id
                client = c
        if id == 0:
            client = dao.add_client(name=name, phone=phone, idcard=id_card)
            print(client)
        return render_template('ticket.html', f=f, list_detail=list_detail, price_list=price_list, client_list=client_list)
    print(price_list)
    return render_template('ticket.html', f=f, list_detail=list_detail, price_list=price_list, client_list=client_list)

@app.route('/api/cart', methods=['GET', 'POST'])
def add_to_cart():
    if 'cart' not in session:
       session['cart'] = {}
    cart = session['cart']
    data = request.json
    id = str(data.get('id'))
    price = int(data.get('price'))
    print(price)
    if id in cart and cart[id]['price'] == price:
        cart[id]['quantity'] = cart[id]['quantity'] + 1
    else:
        cart[id] = {
            'id': id,
            'price': price,
            'quantity': 1
        }

    session['cart'] = cart
    total_quantity, total_amount = dao.cart_stats(session.get('cart'))
    return jsonify({
        'total_quantity': total_quantity,
        'total_amount': total_amount,
        'cart': cart
    })


@app.route('/manage-airport',methods=["GET"])
def airport():
    query = 'SELECT * FROM airport'

    airport = dao.read_data(query)

    return render_template('manage-airport.html', airport=airport)

@app.route('/manage-flight-route')
def route():
    fr = FlightRoute.query.all()
    list_route = []

    for i in fr:
        name1 = Airport.query.add_columns(Airport.name).filter(i.id_airport1 == Airport.id).one()
        name2 = Airport.query.add_columns(Airport.name).filter(i.id_airport2 == Airport.id).one()
        dic = {
            'id': i.id,
            'name1': name1[1],
            'name2': name2[1]
        }
        list_route.append(dic)
    #print(list_route)

    return render_template('manage-flight-route.html', list_route=list_route)
@app.route('/api/client',methods=["GET","POST"])
def ticket():

    if 'client' not in session:
        session['client'] = {}
    detail = session['client']
    data = request.json
    print(data)
    return jsonify('sus')

@app.route('/pay')
def payment():
    total_quantity, total_amount = dao.cart_stats(session.get('cart'))
    return render_template('payment.html', total_quantity=total_quantity, total_amount=total_amount)

@app.route('/add-airport',methods=['GET','POST'])
def add_airport():
    err_msg = ""

    if request.method == 'POST':
        name = request.form.get('NameAirport')
        air = dao.add_airport(name)
        print(air)
        if air:
            err_msg = "Thêm thành công"
            return render_template('add-airport.html', err_msg=err_msg)
        else:
            err_msg = "Đã có sân bay này"
    return render_template('add-airport.html', err_msg=err_msg)

if __name__ == "__main__":
    from mainapp.admin_module import *
    app.run(debug=True, port=8003)