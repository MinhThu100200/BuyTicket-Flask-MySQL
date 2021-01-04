from sqlalchemy import Column, Integer, Float, String, Date, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from mainapp import db
from datetime import datetime
from flask_login import UserMixin

class Airport(db.Model):
    __tablename__ = 'airport'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)

    def __str__(self):
        return self.name

class Plane(db.Model):
    __tablename__ = 'plane'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    amount_of_seat1 = Column(Integer, default=50)
    amount_of_seat2 = Column(Integer, default=50)
    quantity = Column(Integer, default=100)
    flights = relationship('Flight', backref='plane', lazy=True)

    def __str__(self):
        return self.name

class Client(db.Model):
    __tablename__ = 'client'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    phone = Column(String(50), nullable=False)
    idcard = Column(String(50), nullable=False, unique=True)
    tickets = relationship('Ticket', backref='client', lazy=True)
    bookings = relationship('Booking', backref='client', lazy=True)
    bills = relationship('Bill', backref='client', lazy=True)


    def __str__(self):
        return self.name

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    phone = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    active = Column(Boolean, nullable=False, default=True)
    type = Column(Boolean, nullable=False, default=0)
    tickets = relationship('Ticket', backref='user', lazy=True)
    bills = relationship('Bill', backref='user', lazy=True)

    def __str__(self):
        return self.name


class FlightRoute(db.Model):
    __tablename__ = 'flightroute'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    id_airport1 = Column(Integer, default=1)
    id_airport2 = Column(Integer, default=2)
    flights = relationship('Flight', backref='flightroute', lazy=True)



flights_flightdetails_association = db.Table('flight_flightdetail',
    Column('flight_id', Integer, ForeignKey('flight.id'), primary_key=True),
    Column('flightdetail_id', Integer, ForeignKey('flightdetail.id'), primary_key=True)
)


class FlightDetail(db.Model):
    __tablename__ = 'flightdetail'

    id = Column(Integer, primary_key=True, autoincrement=True)
    inter_airport = Column(String(30), default='HongKong')
    waiting_time = Column(Integer, default=0)
    note = Column(String(500))
    flights = relationship('Flight', secondary=flights_flightdetails_association,
                            lazy='subquery', backref=backref('flightdetail', lazy=True))


class Flight(db.Model):
    __tablename__ = 'flight'

    id = Column(Integer, primary_key=True, autoincrement=True)
    date_flight_from = Column(Date, default=datetime.now())
    time_begin = Column(String(20), nullable=False)
    time_end = Column(String(20), nullable=False)
    date_flight_to = Column(Date, default=datetime.now())
    flight_route_id = Column(Integer, ForeignKey(FlightRoute.id), nullable=False)
    plane_id = Column(Integer, ForeignKey(Plane.id), nullable=False)
    tickets = relationship('Ticket', backref='flight', lazy=True)
    bookings = relationship('Booking', backref='flight', lazy=True)
    price_flights = relationship('PriceFlight', backref='fligth', lazy=True)

class PriceFlight(db.Model):
    __tablename__ = 'priceflight'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20))
    vnd = Column(Integer, default=0)
    flight_id = Column(Integer, ForeignKey(Flight.id), nullable=False)
    tickets = relationship('Ticket', backref='priceflight', lazy=True)



typetickets_bookings_association = db.Table('typeticket_booking',
    Column('typeticket_id', Integer, ForeignKey('typeticket.id'), primary_key=True),
    Column('booking_id', Integer, ForeignKey('booking.id'), primary_key=True)
)

class TypeTicket(db.Model):
    __tablename__ = 'typeticket'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    tickets = relationship('Ticket', backref='typeticket', lazy=True)
    bookings = relationship('Booking', secondary=typetickets_bookings_association,
                            lazy='subquery', backref=backref('TypeTicket', lazy=True))



class Ticket(db.Model):
    __tablename__ = 'ticket'

    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(Boolean, default=1)
    price_flight_id = Column(Integer, ForeignKey(PriceFlight.id), nullable=False)
    type_ticket_id = Column(Integer, ForeignKey(TypeTicket.id), nullable=False)
    flight_id = Column(Integer, ForeignKey(Flight.id), nullable=False)
    client_id = Column(Integer, ForeignKey(Client.id), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id))

class Booking(db.Model):
    __tablename__= 'booking'

    id = Column(Integer, primary_key=True, autoincrement=True)
    datetime_booking = Column(Date, default=datetime.now())
    amount_seat = Column(Integer, default=1)
    client_id = Column(Integer, ForeignKey(Client.id), nullable=False)
    flight_id = Column(Integer, ForeignKey(Flight.id), nullable=False)


class Bill(db.Model):
    __tablename__ = 'bill'

    id = Column(Integer, primary_key=True, autoincrement=True)
    datetime_bill = Column(Date, default=datetime.now())
    money = Column(Float, nullable=False, default=400000)
    client_id = Column(Integer, ForeignKey(Client.id), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)

if __name__ == '__main__':
    db.create_all()