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
    name1 = data.get('name1')
    name2 = data.get('name2')
    date_from = data.get('date_from')
    time_begin = data.get('time_begin')
    date_end = data.get('date_end')
    time_end = data.get('time_end')
    amount_of_seat1 = data.get('amount_of_seat1')
    amount_of_seat2 = data.get('amount_of_seat2')
    detail = {
        'id': id,
        'name1': name1,
        'name2': name2,
        'date_from': date_from,
        'time_begin': time_begin,
        'date_end': date_end,
        'time_end': time_end,
        'amount_of_seat1': amount_of_seat1,
        'amount_of_seat2': amount_of_seat2
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

@app.route('/ticket')
def ticket():
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

    for d in dt:
        dic = {
            'inter_airport': d.inter_airport,
            'waiting_time': d.waiting_time,
            'note': d.note
        }

        list_detail.append(dic)
    if request.method == 'POST':
        pass
    # print(f, list_detail)
    return render_template('ticket.html', f=f, list_detail=list_detail)

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

if __name__ == "__main__":
    from mainapp.admin_module import *
    app.run(debug=True, port=5008)