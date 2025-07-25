from django.urls import path


from . import views
from django.contrib.auth.views import LoginView,LogoutView

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
from .forms import UserLoginForm
from .views import  add_package, package_list
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from .views import userdash
# from .views import book_package, packagelist
from .views import book_package, my_bookings, payment_success
from .views import cancel_booking
# from .views import register_provider,login_provider
from .views import payment_successs
from .views import payment_succes
from .views import paymentsuccess
from django.urls import register_converter
from datetime import datetime

class DateConverter:
    regex = r'\d{4}-\d{2}-\d{2}'  # Matches 'YYYY-MM-DD' format

    def to_python(self, value):
        return datetime.strptime(value, "%Y-%m-%d").date()  # Converts to date object

    def to_url(self, value):
        return value.strftime("%Y-%m-%d")  # Converts back to string

register_converter(DateConverter, 'yyyy_mm_dd')


# from .views import book
urlpatterns = [
    path('', views.IndexView, name="home"),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact, name='contact'),
    path('user_login', views.user_login, name='user_login'),
    path('registerss/', views.register, name='registerss'),
    path('verify-packages/', views.verify_packages_admin, name='verify_packages_admin'),
    path('verify-package/<int:package_id>/', views.verify_package, name='verify_package'),
    path('accounts/login/',LoginView.as_view(authentication_form=UserLoginForm),name="login_url"),
    path('register/',views.registerView,name="register_url"),
    path('logout/',LogoutView.as_view(next_page='home'),name="logout"),
    path('package/',views.PackageView,name="package"),
    path('flights/',views.FlightView,name="flights"),
    path('hotels/',views.HotelView,name="hotels"),
    path('places/',views.PlacesView,name="places"),
    # path('bookflight/<str:flight_num>/<str:date>/',views.Flightbook, name='book_flight'),

    path('bookflight/<str:flight_num>/<str:date>/<str:seat_class>/',views.Flightbook,name="bookflight"),
    path('userflight/<str:flight_num>/<str:date>/<int:seat>',views.FlightSubmit,name='userflight'),
    path('bookhotel/<str:hotel>/<str:date>',views.Hotelbook,name="Hotelbook"),
    path('userhotel/<str:hotel>/<str:date>/<int:room>',views.HotelSubmit,name='userflight'),
    path('bookpackage/<str:source>/<str:city>/<str:date>',views.PackageBook,name="bookpackage"),
    path('userpackage/<str:flight>/<str:hotel>/<str:date>/<int:room>/<int:seat>',views.PackageSubmit,name='userpackage'),
    path('cancel-flight/<str:flight_num>/<str:date>/<int:seat>/<str:seat_class>/',views.cancel_flight, name='cancel_flight'),
    

    # path('concanflight/<str:flight>/<str:date>/<int:seat>',views.ConfirmCancelFlight,name='ConfirmCancelFlight'),
    path('cancelhotel/<str:hotel>/<str:date>/<int:room>',views.CancelHotel,name='CancelHotel'),
    path('concanhotel/<str:hotel>/<str:date>/<int:room>',views.ConfirmCancelHotel,name='ConfirmCancelHotel'),
    path("cancel-package/<int:booking_id>/",views.cancel_package, name="cancel_package"),

    # path('cancelpackage/<str:flight>/<int:seat>/<str:hotel>/<str:date>/<int:room>',views.CancelPackage,name='CancelPackage'),
    # path('concanpackage/<str:flight>/<int:seat>/<str:hotel>/<str:date>/<int:room>',views.ConfirmCancelPackage,name='ConfirmCancelPackage'),
    
    # path('accounts/profile/',views.Dashboard,name='dashboard'),
    path('dashboard/',views.Dashboard,name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    
    path('admin-login/', views.admin_login_view, name='admin-login'),
    # path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path('custom_admin_dashboard/', views.custom_admin_dashboard, name='custom_admin_dashboard'),
    path('my-messages/', views.user_messages, name='user_messages'),
    path('messages/delete/<int:message_id>/', views.delete_message, name='delete_message'),
    path('admin/messages/', views.admin_message_list, name='admin_messages_list'),
    path('admin/messages/<int:message_id>/reply/', views.admin_message_reply, name='admin_message_reply'),

    
    
    # path('registers/', register_provider, name='registers'),
    # path('login/', login_provider, name='logins'),

    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('add-package/', add_package, name='add_package'),
    path('packages/', package_list, name='package_list'),
    path('remove_package/<int:package_id>/', views.remove_package, name='remove_package'),
    path('edit/<int:package_id>/', views.edit_package, name='edit_package'), 
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path('book/<int:package_id>/', book_package, name='book_package'),
    path('packagelist/',views.packagelist,name="packagelist"),
    # path('package/<int:package_id>/book/', views.book_package, name='book_package'),
    # path("book/", book, name="book"),
    path('book/<int:package_id>/', book_package, name='book_packages'),
    path('payment-success/', payment_success, name='payment_success'),
    path('cancel-booking/<int:booking_id>/', cancel_booking, name='cancel_booking'),
    path('my-bookings/', my_bookings, name='my_bookings'),
    path("payment-successs/", payment_successs, name="payment_successs"),
    path("payment-succes/", payment_succes, name="payment_succes"),
    path("paymentsuccess/", paymentsuccess, name="paymentsuccess"),
    
    # path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('dashboards/', userdash, name='userdash'),
    path('messages/', views.admin_messages, name='admin_messages'),
    path('messages/reply/<int:message_id>/', views.reply_message, name='reply_message'),

    path('flight/', views.admin_flights, name='admin_flights'),
    path('hotel/', views.admin_hotels, name='admin_hotels'),
    path('pack/', views.admin_packages, name='admin_packages'),
    path('tour-packages/', views.admin_tour_packages, name='admin_tour_packages'),
    path('users/', views.admin_users, name='admin_users'),
    path('providers/', views.admin_providers, name='admin_providers'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns+= staticfiles_urlpatterns()
urlpatterns=urlpatterns+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
