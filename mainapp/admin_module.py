from mainapp import admin, dao
from mainapp.dao import *
from mainapp.models import *
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask_login import current_user, logout_user
from flask import redirect, url_for


class UpdateRule(BaseView):
    @expose('/', methods=['get', 'post'])
    def update(self):
        err_msg = ""
        if request.method == 'POST':
            amount = request.form.get('amount')
            sign = dao.update_rule3(amount)
            if sign == None:
                err_msg = "Điều chỉnh không thành công"
                return self.render('/admin/rule3.html', err_msg=err_msg)
        err_msg = "Điều chỉnh thành công"
        return self.render('/admin/rule3.html', err_msg=err_msg)

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect('/admin')

class RevenueMonth(BaseView):
    @expose('/', methods=['get', 'post'])
    def revenue_month(self):
        err_msg = ""
        list_flight = []
        if request.method == 'POST':
            month = request.form.get('month')
            year = request.form.get('year')
            list_flight = dao.revenue_month(month, year)
            print(list_flight)
            return self.render('/admin/report_month.html', err_msg=err_msg, list_flight=list_flight)
        return self.render('/admin/report_month.html', err_msg=err_msg)

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect('/admin')

class RevenueYear(BaseView):
    @expose('/', methods=['get', 'post'])
    def revenue_month(self):
        err_msg = ""
        list_month = []
        if request.method == 'POST':
            year = request.form.get('year')
            list_month = dao.revenue_year(year)
            print(list_month)
            return self.render('/admin/report_year.html', err_msg=err_msg, list_month=list_month)
        return self.render('/admin/report_year.html', err_msg=err_msg)

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect('/admin')


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
                err_msg = "Mật khẩu không trùng khớp"
            else:
                if dao.add_employee(name=name, email=email, phone=phone, username=username, password=password):
                    err_msg = "Đăng ký thành công"
                    return self.render('/admin/register.html', err_msg=err_msg)
                else:
                    err_msg = "Đăng ký không thành công"
                    return self.render('/admin/register.html', err_msg=err_msg)

        return self.render('/admin/register.html')

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect('/admin')

class ChartView(BaseView):
    @expose('/', methods=['get', 'post'])
    def report(self):
        if request.method == 'GET':
            return self.render('/admin/chart.html')

        if request.method == 'POST':
            type = request.form.get('typechart')
            return self.render('/admin/chart.html', chartJSON=draw_chart(type))
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect('/admin')

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

class BookingViewModel(ModelView):
    column_display_pk = True

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect('/admin')

class PriceFlightModelView(ModelView):

    column_display_pk = True
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect('/admin')


admin.add_view(FlightModelView(Flight, db.session))
admin.add_view(UserModelView(User, db.session))
admin.add_view(FlightDetailModelView(FlightDetail, db.session))
admin.add_view(BookingViewModel(Booking, db.session))
admin.add_view(FlightRouteModelView(FlightRoute, db.session))
#admin.add_view(ModelView(Plane, db.session))
admin.add_view(PriceFlightModelView(PriceFlight, db.session))
#admin.add_view(ModelView(Bill, db.session))
#admin.add_view(ModelView(Ticket, db.session))
#admin.add_view(ModelView(TypeTicket, db.session))
admin.add_view(AirportModelView(Airport, db.session))
admin.add_view(UpdateRule(name='UpdateRule'))
admin.add_view(ChartView(name="CHART"))
admin.add_view(RevenueMonth(name='RevenueMonth'))
admin.add_view(RevenueYear(name='RevenueYear'))
admin.add_view(AboutUs(name="About Us"))
admin.add_view(SignupModelView(name="Signup"))
admin.add_view(LogoutView(name="Logout"))

