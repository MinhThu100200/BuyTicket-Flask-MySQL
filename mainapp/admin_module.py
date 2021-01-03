from mainapp import admin, dao
from mainapp.dao import *
from mainapp.models import *
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask_login import current_user, logout_user
from flask import redirect, url_for
import pymysql
from pychartjs import BaseChart, ChartType, Color

class SignupModelView(BaseView):
    @expose('/', methods=['get', 'post'])
    def signup(self):
        err_msg = ""
        if request.method == "POST":
            name = request.form.get("name")
            email = request.form.get("email")
            phone = request.form.get("phone")
            username = request.form.get("username")
            password = request.form.get("password")
            confirm = request.form.get("confirm")
            if password.strip() != confirm.strip():
                err_msg = "Mat khau khong trung khop"
            else:
                if dao.add_employee(name=name, email=email, phone=phone, username=username, password=password):
                    err_msg = "Dang ky thanh cong"
                    return self.render('/admin/register.html', err_msg=err_msg)
                else:
                    err_msg = "Dang ky khong thanh cong"
                    return self.render('/admin/register.html', err_msg=err_msg)

        return self.render('/admin/register.html')

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect('/admin')

'''class ReportMonthView(BaseView):
    @expose('/', methods=['get','post'])
    def report(self):

        if request.method == 'GET':
            return self.render('/admin/chart.html')

        if request.method == 'POST':
            type = request.form.get('typechart')
            if type == '1':
                #print(ChartJSON)
                return draw_chart()
            else:
                return redirect('/admin')
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect('/admin')
'''
class AboutUs(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/about-us.html')


    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect('/admin')

class UserModelView(ModelView):
    column_display_pk = True
    #can_create = False
    form_columns = ('name', 'email', 'phone', 'username', 'password', 'active', 'type',)
    column_searchable_list = ['id', 'name', 'username']

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect('/admin')

class AirportModelView(ModelView):
    column_display_pk = True
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect('/admin')


class FlightModelView(ModelView):
    column_display_pk = True
    column_searchable_list = ['id', 'date_flight_from']
    inline_models = [FlightDetail]

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect('/admin')


class FlightRouteModelView(ModelView):
    column_display_pk = True
    column_searchable_list = ['id']
    inline_models = [Flight]

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect('/admin')


class FlightDetailModelView(ModelView):
    column_display_pk = True
    column_searchable_list = ['id']
    inline_models = [Flight]
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect('/admin')

class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/')

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect('/admin')

class ReportYearView(BaseView):
    @expose('/')
    def report(self):
        return self.render('admin/revenue.html')

    def is_accessible(self):
        return current_user.is_authenticated
    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect('/admin')

class BookingViewModel(ModelView):
    column_display_pk = True

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect('/admin')

class RevenueMonthViewModel(ModelView):
    column_display_pk = True
    can_export = True
    can_set_page_size = True
    column_searchable_list = ['id', 'revenue_year_id']

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect('/admin')

class RevenueYearViewModel(ModelView):
    column_display_pk = True
    can_export = True
    can_set_page_size = True
    column_searchable_list = ['id']

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect('/admin')



admin.add_view(FlightModelView(Flight, db.session))
admin.add_view(UserModelView(User, db.session))
admin.add_view(FlightDetailModelView(FlightDetail, db.session))
admin.add_view(BookingViewModel(Booking, db.session))
admin.add_view(AboutUs(name="About Us"))
admin.add_view(FlightRouteModelView(FlightRoute, db.session))
admin.add_view(SignupModelView(name="Signup"))
admin.add_view(LogoutView(name="Logout"))
admin.add_view(ModelView(Plane, db.session))
admin.add_view(ModelView(PriceFlight, db.session))
admin.add_view(ModelView(Bill, db.session))
admin.add_view(ModelView(Ticket, db.session))
admin.add_view(ModelView(TypeTicket, db.session))
admin.add_view(AirportModelView(Airport, db.session))
admin.add_view(ModelView(Client, db.session))

