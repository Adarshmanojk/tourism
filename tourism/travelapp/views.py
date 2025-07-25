from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from .models import *

from django.contrib.auth.decorators import login_required
from django.contrib import admin
from .models import ContactMessage

from .forms import SignUpForm,HotelForm,FlightForm,ChoiceForm,SeatForm,RoomForm,CityForm
from .models import Flights,Hotels,Famous,BookFlight,BookHotel,BookPackage,City
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import TourPackage, Booking
from .forms import BookingForm 
# Create your views here.
def IndexView(request):
    return render(request,'index.html')
def about_view(request):
    return render(request, 'about.html')

from django.contrib import messages
from .models import ContactMessage

class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at', 'replied_at')
    readonly_fields = ('name', 'email', 'message', 'created_at')
    search_fields = ('name', 'email', 'message')
    list_filter = ('created_at',)

    fieldsets = (
        ("User Info", {
            "fields": ('name', 'email')
        }),
        ("Message Details", {
            "fields": ('message', 'created_at')
        }),
        ("Admin Reply", {
            "fields": ('reply', 'replied_at')
        }),
    )

    def save_model(self, request, obj, form, change):
        if obj.reply and not obj.replied_at:
            from django.utils import timezone
            obj.replied_at = timezone.now()
        super().save_model(request, obj, form, change)


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message_text = request.POST.get('message')

        if name and email and message_text:
            ContactMessage.objects.create(
                user=request.user if request.user.is_authenticated else None,
                name=name,
                email=email,
                message=message_text
            )
            messages.success(request, "Thank you for contacting us! We'll get back to you soon.")
        else:
            messages.error(request, "Please fill all fields.")

    return render(request, 'contact.html')


@login_required
def user_messages(request):
    messages = ContactMessage.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'user_messages.html', {'messages': messages})

from django.contrib import messages as msg_system
from django.shortcuts import get_object_or_404, redirect
from .models import ContactMessage  # or whatever your model is

@login_required
def delete_message(request, message_id):
    message = get_object_or_404(ContactMessage, id=message_id, user=request.user)
    if request.method == "POST":
        message.delete()
        msg_system.success(request, "Message deleted successfully.")
    return redirect('user_messages')


from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def admin_message_list(request):
    messages = ContactMessage.objects.all().order_by('-created_at')
    return render(request, 'admin_messages_list.html', {'messages': messages})
@staff_member_required
def admin_message_reply(request, message_id):
    msg = get_object_or_404(ContactMessage, id=message_id)

    if request.method == 'POST':
        reply = request.POST.get('reply')
        msg.reply = reply
        msg.replied_at = timezone.now()
        msg.save()
        messages.success(request, 'Reply sent successfully!')
        return redirect('admin_messages_list')

    return render(request, 'admin_reply.html', {'message': msg})
from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u: u.is_superuser)
def admin_message_list(request):
    ...
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

def admin_login_view(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('custom_admin_dashboard')  # ✅ FIXED

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            return redirect('custom_admin_dashboard')  # ✅ FIXED
        else:
            messages.error(request, "Invalid credentials or not authorized as admin.")

    return render(request, 'admin_login.html')


from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.shortcuts import render
from .models import BookFlight, BookHotel, BookPackage, Booking, Flights, Hotels, TourPackage, ContactMessage

@staff_member_required
def custom_admin_dashboard(request):
    context = {
        'total_users': get_user_model().objects.count(),
        'total_packages': TourPackage.objects.count(),
        'total_flights': Flights.objects.count(),
        'total_hotels': Hotels.objects.count(),
        'latest_messages': ContactMessage.objects.all().order_by('-created_at')[:5],
        'latest_flight_bookings': BookFlight.objects.select_related('username_id').order_by('-id')[:5],
        'latest_hotel_bookings': BookHotel.objects.select_related('username_id').order_by('-id')[:5],
        'latest_package_bookings': BookPackage.objects.select_related('username_id').order_by('-id')[:5],
        'latest_tour_bookings': Booking.objects.select_related('user', 'package').order_by('-id')[:5],
    }
    return render(request, 'custom_admin_dashboard.html', context)

from django.shortcuts import render
from .models import ContactMessage, BookFlight, BookHotel, BookPackage, Booking, Flights, Hotels, TourPackage

# Admin main navigation dashboard
# def admin_dashboard(request):
#     return render(request, 'admin_dashboard/admin_navigation.html')

from django.contrib.auth.models import User
from django.shortcuts import render

def admin_users(request):
    users = User.objects.filter(is_staff=False, is_superuser=False).exclude(provider_profile__isnull=False)
    return render(request, 'admin_users.html', {'users': users})

# def admin_users(request):
#     users = User.objects.filter(is_staff=False)  # Excludes staff users
#     return render(request, 'admin_users.html', {'users': users})

def admin_providers(request):
    providers = provider.objects.all()
    return render(request, 'admin_providers.html', {'providers': providers})

from django.shortcuts import render
from .models import TourPackage
from django.contrib.auth.decorators import login_required

@login_required
def verify_packages_admin(request):
    if not request.user.is_staff:
        return redirect('custom_admin_dashboard')  # Restrict access to admin only

    packages = TourPackage.objects.all()  # Show all packages, including verified ones
    return render(request, 'admin_verify_packages.html', {'packages': packages})

from django.shortcuts import redirect, get_object_or_404


@login_required
def verify_package(request, package_id):
    if not request.user.is_staff:
        return redirect('custom_admin_dashboard')

    packages = get_object_or_404(TourPackage, id=package_id)
    packages.verified = True
    packages.availability = True  # Ensure the package is available
    packages.save()
    
    return redirect('verify_packages_admin')  # Ensure this matches urls.py
 # Redirect to the correct page
from .models import TourPackage
@login_required
def package_list(request):
    if request.user.is_staff:  # Admins can see all packages
        packages = TourPackage.objects.all()
    else:  # Providers only see their own packages
        packages = TourPackage.objects.filter(provider=request.user)
    
    return render(request, 'package_list.html', {'packages': packages})
from .models import TourPackage
def packagelist(request):
    # packages = TourPackage.objects.filter(verified=True, availability=True)
    packages = TourPackage.objects.all()  # Show everything
    return render(request, 'packagelist.html', {'packages': packages})

#📬 Messages View
def admin_messages(request):
    latest_messages = ContactMessage.objects.all().order_by('-created_at')
    return render(request, 'messages.html', {
        'latest_messages': latest_messages
    })
# def admin_messages(request):
#     return render(request, 'messages.html')
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from .models import ContactMessage  # Make sure this is correct

def reply_message(request, message_id):
    msg = get_object_or_404(ContactMessage, id=message_id)

    if request.method == 'POST':
        reply_text = request.POST.get('reply')
        msg.reply = reply_text
        msg.replied_at = timezone.now()
        msg.save()
        messages.success(request, 'Reply saved successfully.')
        return redirect('admin_messages')

    return render(request, 'admin_reply_message.html', {'message': msg})



# 🛫 Flights View
def admin_flights(request):
    latest_flight_bookings = BookFlight.objects.select_related('username_id').order_by('-date')
    return render(request, 'adminflights.html', {
        'latest_flight_bookings': latest_flight_bookings
    })


# 🏨 Hotels View
def admin_hotels(request):
    latest_hotel_bookings = BookHotel.objects.select_related('username_id').order_by('-date')
    return render(request, 'adminhotels.html', {
        'latest_hotel_bookings': latest_hotel_bookings
    })


# 📦 Packages (Flight + Hotel) View
def admin_packages(request):
    latest_package_bookings = BookPackage.objects.select_related('username_id').order_by('-date')
    return render(request, 'adminpackages.html', {
        'latest_package_bookings': latest_package_bookings
    })


# 🌍 Tour Packages View
from .models import Booking

def admin_tour_packages(request):
    latest_tour_bookings = Booking.objects.select_related('user', 'package').order_by('-booking_date')
    return render(request, 'admintourpackages.html', {
        'latest_tour_bookings': latest_tour_bookings
    })


def PackageView(request):
    form = FlightForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            source = form.cleaned_data['source'].upper()
            date = form.cleaned_data['date']
            destination = form.cleaned_data['destination'].upper()

            # Query the database
            flights = Flights.objects.filter(source=source, destination=destination)
            famplace = Famous.objects.filter(city__city__icontains=destination)
            hotels = Hotels.objects.filter(city__city__icontains=destination)

            # Safely get the city from hotels
            if hotels.exists():  # Check if hotels queryset is not empty
                j = hotels[0].city
            else:
                j = None  # Handle the case where no hotels are found

            # Prepare context for the template
            context = {
                'Flights': flights,
                'source': source,
                'Hotels': hotels,
                'Famplace': famplace,
                'form': form,
                'date': date,
                'city': j,  # Can be None if no hotels are found
            }
            return render(request, 'package.html', context)

    # Handle GET or invalid form POST
    return render(request, 'package.html', {'form': form})



def registerView(request):
    if request.method=="POST":
        form=SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_url')
    else:
            form=SignUpForm()
    return render(request,'registration/register.html',{'form': form})

def HotelView(request):
    form = HotelForm(request.POST)
    if request.method=="POST":
        if form.is_valid():
            city = form.cleaned_data['city'].upper()
            date = form.cleaned_data['date']
            hotels = Hotels.objects.filter(city__city__contains=city)
            d = {'date':date}
            h = {'Hotels':hotels}
            form = {'form': form}
            response = {**h,**d,**form}
            return render(request,'hotels.html',response)
        else:
            return render(request,'hotels.html',{'form': form})

    else:
        return render(request,'hotels.html',{'form': form})

def FlightView(request):
    form = FlightForm(request.POST)
    c = 0;
    if request.method=="POST":
        if form.is_valid():
            source = form.cleaned_data['source'].upper()
            destination = form.cleaned_data['destination'].upper()
            date = form.cleaned_data['date']
            flights = Flights.objects.filter(source=source).filter(destination=destination)
            d = {'date':date}
            f = {'Flights':flights}
            form = {'form': form}
            response = {**f,**d,**form}
            return render(request,'flights.html',response)
        else:
            return render(request,'flights.html',{'form': form})
    else:
        return render(request,'flights.html',{'form': form})
    
def PlacesView(request):
    return render(request,'places.html')
@login_required
def Dashboard(request):
    user = request.user
    f1 = BookFlight.objects.filter(username_id=user)
    h1 = BookHotel.objects.filter(username_id=user)
    p1 = BookPackage.objects.filter(username_id=user)
    f={'flights':f1}
    h={'hotels':h1}
    p={'packages':p1}
    response= {**f,**h,**p}
    return render(request,'dashboard.html',response)
def logout_view(request):
     logout(request)
     return redirect('home')


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Flights, BookFlight, BookPackage
from .forms import SeatForm


from datetime import datetime
from .models import Flights, BookFlight, BookPackage
from .forms import SeatForm

# Initialize Razorpay client
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

@login_required
def Flightbook(request, flight_num=None, date=None, seat_class=None):
    try:
        # Convert date to YYYY-MM-DD format
        date = datetime.strptime(date, "%B %d, %Y").strftime("%Y-%m-%d")
    except ValueError:
        return render(request, "error.html", {"error": "Invalid date format. Please use YYYY-MM-DD."})

    cs_economy = 0  # Counter for booked economy seats
    cs_business = 0  # Counter for booked business seats
    seatrem_economy = 0
    seatrem_business = 0
    avail_economy = "unavailable"
    avail_business = "unavailable"
    price = 0

    form = SeatForm(request.POST or None)
    flight = get_object_or_404(Flights, flight_num=flight_num)

    # Get booked seats for this date
    # booked_flights = BookFlight.objects.filter(flight=flight_num, date=date)
    # booked_packages = BookPackage.objects.filter(flight=flight_num, date=date)
    flight = get_object_or_404(Flights, flight_num=flight_num)  # ✅ Fetch the flight instance
    booked_flights = BookFlight.objects.filter(flight=flight, date=date)
    booked_packages = BookPackage.objects.filter(flight=flight, date=date)

    for booking in booked_flights:
        if booking.seat_class == "economy":
            cs_economy += booking.seat
        elif booking.seat_class == "business":
            cs_business += booking.seat

    for package in booked_packages:
        if package.seat_class == "economy":
            cs_economy += package.seat
        elif package.seat_class == "business":
            cs_business += package.seat

    # Calculate remaining seats
    seatrem_economy = flight.economy_seats - cs_economy
    seatrem_business = flight.business_seats - cs_business

    # Set availability status
    if seatrem_economy > 0:
        avail_economy = "available"
    if seatrem_business > 0:
        avail_business = "available"

    if request.method == "POST" and form.is_valid():
        seats = form.cleaned_data['seats']

        # Determine price based on seat class
        if seat_class == "economy":
            price = seats * flight.eprice
            if seatrem_economy < seats:
                return render(request, "bookflight.html", {"error": "Not enough economy seats available"})
        elif seat_class == "business":
            price = seats * flight.bprice
            if seatrem_business < seats:
                return render(request, "bookflight.html", {"error": "Not enough business seats available"})

        # **Create Razorpay Order**
        amount = int(price * 100)  # Convert to paise
        data = {"amount": amount, "currency": "INR", "payment_capture": "1"}
        order = client.order.create(data=data)

        response = {
            "flight": flight,
            "date": date,
            "form": form,
            "seatrem_economy": seatrem_economy,
            "seatrem_business": seatrem_business,
            "availability_economy": avail_economy,
            "availability_business": avail_business,
            "seatsreq": seats,
            "seat_class": seat_class,
            "price": price,
            "total_price": price,  # ✅ Pass total price explicitly
            "razorpay_order_id": order["id"],
            "razorpay_key": settings.RAZORPAY_KEY_ID,
        }
        return render(request, "bookflight.html", response)

    return render(request, "bookflight.html", {
        "form": form,
        "flight": flight,
        "date": date,
        "seat_class": seat_class,
        "seatrem_economy": seatrem_economy,
        "seatrem_business": seatrem_business,
        "availability_economy": avail_economy,
        "availability_business": avail_business,
    })


@csrf_exempt
def payment_successs(request):
    if request.method == "POST":
        payment_id = request.POST.get("razorpay_payment_id")
        order_id = request.POST.get("razorpay_order_id")
        signature = request.POST.get("razorpay_signature")
        flight_num = request.POST.get("flight_num")
        date = request.POST.get("date")  # Ensure format YYYY-MM-DD
        seats = int(request.POST.get("seats", 1))  # Default seat count
        seat_class = request.POST.get("seat_class", "economy")  # Default to economy

        user = request.user  # ✅ Get the logged-in user

        print(f"Received Payment: {payment_id}, {order_id}, Flight: {flight_num}, Date: {date}, Seats: {seats}, Class: {seat_class}")

        try:
            # Verify payment signature
            client.utility.verify_payment_signature({
                "razorpay_order_id": order_id,
                "razorpay_payment_id": payment_id,
                "razorpay_signature": signature
            })

            print("✅ Payment verification successful!")

            if not user.is_authenticated:
                return JsonResponse({"status": "failure", "message": "User authentication failed."})
            
            flight_instance = get_object_or_404(Flights, flight_num=flight_num)  # ✅ Fetch the flight instance
            # Save booking in the database
            booking = BookFlight.objects.create(
                username_id=user,
                flight=flight_instance, 
                date=date,
                seat=seats,
                seat_class=seat_class
            )
            print("✅ Booking saved successfully:", booking)

            return JsonResponse({"status": "success", "redirect_url": "/dashboard/"})

        except razorpay.errors.SignatureVerificationError:
            print("❌ Payment verification failed!")
            return JsonResponse({"status": "failure", "message": "Payment verification failed."})


@login_required
def FlightSubmit(request, flight_num=None, date=None, seat=None, seat_class="economy"):
    user = request.user

    # Ensure valid seat_class
    if seat_class not in ["economy", "business"]:
        messages.error(request, "Invalid seat class selected.")
        return redirect("dashboard")

    # Get booked seats for the selected date
    booked_flights = BookFlight.objects.filter(flight=flight_num, date=date, seat_class=seat_class).aggregate(
        total_seats=models.Sum('seat'))['total_seats'] or 0

    # Get flight details
    flight = get_object_or_404(Flights, flight_num=flight_num)

    # Check seat availability
    if seat_class == "economy":
        remaining_seats = flight.economy_seats - booked_flights
    else:  # business
        remaining_seats = flight.business_seats - booked_flights

    if remaining_seats < seat:
        messages.error(request, "Not enough seats available.")
        return redirect("dashboard")

    # Save booking
    flight = get_object_or_404(Flights, flight_num=flight_num)  # ✅ Fetch the flight instance
    booking = BookFlight(username_id=user, flight=flight, date=date, seat=seat, seat_class=seat_class)  # ✅ Correct

    # booking = BookFlight(username_id=user, flight=flight_num, date=date, seat=seat, seat_class=seat_class)
    booking.save()
    messages.success(request, "Flight booked successfully!")

    return redirect("dashboard")


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime
from .models import BookFlight

@login_required
def cancel_flight(request, flight_num=None, date=None, seat=None, seat_class=None):
    """Handles flight cancellation by the user."""
    try:
        # Convert date format
        formatted_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        messages.error(request, "Invalid date format.")
        return redirect("dashboard")

    # Fetch a single booking, avoiding MultipleObjectsReturned
    booking = (
        BookFlight.objects.filter(
            username_id=request.user.id,  # Ensure correct field
            flight=flight_num,
            date=formatted_date,
            seat=seat,
            seat_class=seat_class,
        )
        .first()  # ✅ Gets the first matching record, avoiding errors
    )

    if not booking:
        messages.error(request, "No matching booking found.")
        return redirect("dashboard")

    if request.method == "POST":
        booking.delete()
        messages.success(request, "Your flight booking has been canceled successfully.")
        return redirect("dashboard")

    return render(request, "confirm_cancel.html", {"booking": booking})


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Hotels, BookHotel, BookPackage
from .forms import RoomForm



# Initialize Razorpay client
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

@login_required
def Hotelbook(request, hotel, date):
    cs = 0  # Counter for booked rooms
    price = 0
    roomrem = 0
    avail = "unavailable"

    form = RoomForm(request.POST or None)
    
    # Fetch the hotel object using 'hotel' from the URL
    hotel_obj = get_object_or_404(Hotels, hotel_name__iexact=hotel)

    # 🔹 Convert the date to YYYY-MM-DD format
    try:
        date = datetime.strptime(date, "%B %d, %Y").strftime("%Y-%m-%d")
    except ValueError:
        messages.error(request, "Invalid date format! Use YYYY-MM-DD.")
        return redirect("dashboard")

    if request.method == "POST" and form.is_valid():
        rooms = form.cleaned_data['rooms']

        # 🔹 Calculate remaining rooms
        booked_hotels = BookHotel.objects.filter(hotel_name=hotel_obj, date=date)
        booked_packages = BookPackage.objects.filter(hotel_name=hotel_obj, date=date)

        for booking in booked_hotels:
            cs += booking.room
        for package in booked_packages:
            cs += package.room

        roomrem = hotel_obj.rooms - cs
        price = rooms * hotel_obj.hotel_price  # ✅ Calculate total price

        if (roomrem - rooms) >= 0:
            avail = "available"

        # ✅ Create Razorpay Order
        try:
            amount = int(price * 100)  # Convert to paise
            data = {"amount": amount, "currency": "INR", "payment_capture": "1"}
            order = client.order.create(data=data)
        except Exception as e:
            messages.error(request, f"Razorpay order creation failed: {str(e)}")
            return redirect("dashboard")

        # ✅ Pass order details to the template
        response = {
            "hotel": [hotel_obj],
            "date": date,
            "form": form,
            "roomrem": roomrem,
            "availability": avail,
            "roomsreq": rooms,
            "price": price,
            "razorpay_order_id": order["id"],
            "razorpay_key": settings.RAZORPAY_KEY_ID,
        }
        return render(request, "bookhotel.html", response)

    return render(request, "bookhotel.html", {"form": form})


@login_required
def payment_succes(request):
    if request.method == "POST":
        try:
            # Get Razorpay payment details
            razorpay_payment_id = request.POST.get("razorpay_payment_id")
            razorpay_order_id = request.POST.get("razorpay_order_id")
            razorpay_signature = request.POST.get("razorpay_signature")
            hotel_name = request.POST.get("hotel_name")
            date = request.POST.get("date")
            rooms = int(request.POST.get("rooms"))

            # Get the hotel object
            hotel_obj = get_object_or_404(Hotels, hotel_name=hotel_name)

            # 🔹 Recalculate total price
            total_price = rooms * hotel_obj.hotel_price

            # Save the booking
            booking = BookHotel.objects.create(
                username_id=request.user,
                hotel_name=hotel_obj,  # ✅ If it's a ForeignKey
                date=date,
                room=rooms,
                total_price=total_price  # ✅ Save total price
            )

            print("✅ Booking saved successfully:", booking)

            return JsonResponse({"status": "success", "message": "Booking confirmed!"})

        except Exception as e:
            print(f"❌ Payment processing error: {e}")
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)



@login_required
def HotelSubmit(request,hotel=None,date=None,room=None):
    user = request.user
    b = BookHotel(username_id=user,hotel_name=hotel,date=date,room=room)
    b.save()
    return redirect('dashboard')

@login_required
def CancelHotel(request, hotel=None, date=None, room=None):
    hotel_obj = Hotels.objects.filter(hotel_name=hotel).first()  # ✅ Get the first match
    
    if not hotel_obj:
        messages.error(request, "Hotel not found!")
        return redirect('dashboard')

    price = int(room) * hotel_obj.hotel_price  # ✅ Convert `room` to int

    response = {
        'Hotel': [hotel_obj],
        'price': price,
        'room': room,
        'date': date
    }
    return render(request, 'cancelhotel.html', response)
from datetime import datetime

from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect

@login_required
def ConfirmCancelHotel(request, hotel=None, date=None, room=None):
    user = request.user
    
    # Convert date format from 'May 8, 2025' to '2025-05-08'
    try:
        formatted_date = datetime.strptime(date, "%B %d, %Y").strftime("%Y-%m-%d")
    except ValueError:
        return HttpResponse("Invalid date format", status=400)

    # Get the Hotel object using hotel_name
    hotel_obj = get_object_or_404(Hotels, hotel_name=hotel)

    # Fetch the booked hotel entry (use hotel_name as a string, not hotel_obj)
    hotel_booking = BookHotel.objects.filter(
        username_id=user,
        hotel_name=hotel_obj.id,  # Use the hotel's id instead of name if it's a ForeignKey
        date=formatted_date,  # Use corrected date format
        room=room
    )

    if hotel_booking.exists():
        hotel_booking.delete()
        return redirect('dashboard')
    else:
        return HttpResponse("No matching booking found", status=404)




import razorpay
import json
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .models import Flights, Hotels, BookPackage, BookFlight, BookHotel
from .forms import ChoiceForm
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import razorpay
from django.conf import settings
from django.contrib import messages
from .models import BookPackage
from datetime import datetime

@login_required
def PackageBook(request, source, city, date):
    try:
        date = datetime.strptime(date, "%B %d, %Y").strftime("%Y-%m-%d")
    except ValueError:
        return HttpResponse("Invalid date format", status=400)

    form = ChoiceForm(request.POST or None)
    allf = Flights.objects.filter(source=source, destination=city)
    allh = Hotels.objects.filter(city__city__contains=city)

    if request.method == "POST" and form.is_valid():
        flight_num = form.cleaned_data['flight'].upper()
        hotel_name = form.cleaned_data['hotel']
        seats = form.cleaned_data['seats']
        room = form.cleaned_data['rooms']
        seat_class = form.cleaned_data['seat_class']

        # Fetch the hotel by hotel_name and get its id
        hotel = get_object_or_404(Hotels, hotel_name=hotel_name)
        hotel_id = hotel.id  # Extract hotel id
        
        flight = get_object_or_404(Flights, flight_num=flight_num)

        cs = sum(booking.seat for booking in BookFlight.objects.filter(flight=flight, date=date))
        cs += sum(package.seat for package in BookPackage.objects.filter(flight=flight, date=date))

        seatrem = flight.economy_seats if seat_class == "economy" else flight.business_seats
        seatrem -= cs  # Remaining seats

        price_flight = seats * flight.eprice if seat_class == "economy" else seats * flight.bprice
        availf = "available" if seatrem >= seats else "unavailable"

        # Corrected: Use hotel_id to filter BookHotel
        cs1 = sum(booking.room for booking in BookHotel.objects.filter(hotel_name_id=hotel_id, date=date))
        cs1 += sum(package.room for package in BookPackage.objects.filter(hotel_name_id=hotel_id, date=date))

        roomrem = hotel.rooms - cs1
        price_hotel = room * hotel.hotel_price
        availh = "available" if roomrem >= room else "unavailable"

        total_amount = int((price_flight + price_hotel) * 100)  # Convert to paisa
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        payment_order = client.order.create({
            "amount": total_amount,
            "currency": "INR",
            "receipt": f"booking_{request.user.id}_{date}",
            "payment_capture": 1,
        })

        context = {
            "Flights": [flight], "Hotels": [hotel], "allflights": allf, "allhotels": allh, "form": form,
            "flavailability": availf, "pricef": price_flight, "seatsreq": seats, "seatrem": seatrem,
            "havailability": availh, "priceh": price_hotel, "roomreq": room, "roomrem": roomrem,
            "date": date, "razorpay_order_id": payment_order["id"],
            "razorpay_key": settings.RAZORPAY_KEY_ID, "total_amount": total_amount // 100,
            "selected_seat_class": seat_class,  # Pass the selected seat class to the template
        }
        return render(request, "bookpackage.html", context)

    return render(request, "bookpackage.html", {"allflights": allf, "allhotels": allh, "form": form})




@csrf_exempt
def paymentsuccess(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            print("Received data:", data)

            payment_id = data.get("razorpay_payment_id")
            order_id = data.get("razorpay_order_id")
            signature = data.get("razorpay_signature")

            # Log values
            print(f"Payment ID: {payment_id}, Order ID: {order_id}, Signature: {signature}")

            if not all([payment_id, order_id, signature]):
                return JsonResponse({"status": "Invalid payment data received"}, status=400)

            # Verify Razorpay payment signature
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            params_dict = {
                "razorpay_order_id": order_id,
                "razorpay_payment_id": payment_id,
                "razorpay_signature": signature,
            }

            # Razorpay signature verification
            try:
                client.utility.verify_payment_signature(params_dict)
                print("✅ Payment signature verified successfully")
            except razorpay.errors.SignatureVerificationError as e:
                print(f"❌ Signature verification failed: {str(e)}")
                return JsonResponse({"status": "Payment verification failed!"}, status=400)

            # Log received fields
            print(f"Seats: {data.get('seats')}, Flight Number: {data.get('flight_number')}, Hotel Name: {data.get('hotel_name')}, Rooms: {data.get('rooms')}, Date: {data.get('date')}, Seat Class: {data.get('seat_class')}")

            seats = data.get("seats")
            flight_number = data.get("flight_number")
            hotel_name = data.get("hotel_name")
            rooms = data.get("rooms")
            date = data.get("date")
            seat_class = data.get("seat_class")

            if not all([seats, flight_number, hotel_name, rooms, date, seat_class]):
                return JsonResponse({"status": "Missing booking details"}, status=400)

            # Assuming user is authenticated
            user = request.user

            # Fetch the Flights instance using the flight number
            flight_instance = get_object_or_404(Flights, flight_num=flight_number)

            # Fetch the Hotels instance using the hotel name
            hotel_instance = get_object_or_404(Hotels, hotel_name=hotel_name)

            # Create booking record
            booking = BookPackage.objects.create(
                username_id=user,  # Ensure you're using 'username_id' to link user
                seat=int(seats),
                flight=flight_instance,  # ✅ Use the fetched Flights instance
                hotel_name=hotel_instance,  # ✅ Use the fetched Hotels instance
                room=int(rooms),
                date=date,
                seat_class=seat_class
            )

            print("✅ Booking saved successfully:", booking)
            messages.success(request, "Payment successful! Your booking has been confirmed.")
            return JsonResponse({"status": "Payment successful!", "booking_id": booking.id, "redirect_url": "/dashboard/"})

        except json.JSONDecodeError:
            return JsonResponse({"status": "Invalid JSON format"}, status=400)
        except Exception as e:
            print(f"❌ Error in paymentsuccess: {e}")
            return JsonResponse({"status": "Server error", "error": str(e)}, status=500)

    return JsonResponse({"status": "Invalid request method"}, status=400)




@login_required
def PackageSubmit(request,flight=None,hotel=None,date=None,seat=None,room=None):
    user = request.user
    b = BookPackage(username_id=user,flight=flight,seat=seat,hotel_name=hotel,room=room,date=date)
    b.save()
    return redirect('dashboard')

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import BookPackage  # Ensure you import your model

@login_required
def cancel_package(request, booking_id):
    booking = get_object_or_404(BookPackage, id=booking_id, username_id=request.user)

    if request.method == "POST":
        booking.delete()
        messages.success(request, "Your package booking has been successfully canceled.")
        return redirect("dashboard")  # Redirect instead of JSON response

    return render(request, "cancelpackage.html", {"booking": booking})  # Render the cancel page






from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import BookPackage  # Import your model for package bookings


from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .models import provider  # Import Provider model

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Check if the user is registered as a provider
            if hasattr(user, 'provider_profile'):  
                login(request, user)
                return redirect('package_list')  # Redirect to provider dashboard
            else:
                return render(request, 'user/login.html', {'error': 'Access denied: Only providers can log in.'})
        else:
            return render(request, 'user/login.html', {'error': 'Invalid username or password'})

    return render(request, 'user/login.html')

from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import render, redirect
from .models import provider

def register(request):
    if request.method == "POST":
        name = request.POST.get("name", "")
        phone = request.POST.get("phone", "")
        email = request.POST.get("email", "")
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")

        if User.objects.filter(username=username).exists():
            return render(request, "user/register.html", {"error": "Username already taken"})
        
        if User.objects.filter(email=email).exists():
            return render(request, "user/register.html", {"error": "Email already registered"})

        # Create a new user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = name
        user.save()

        # Create a provider profile
        provider.objects.create(user=user, phone=phone)

        # Redirect to login page after successful registration
        return redirect('user_login')  # Ensure 'user_login' is the correct URL name for your login view

    return render(request, "user/register.html")

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import TourPackageForm

@login_required
def add_package(request):
    if request.method == 'POST':
        # Include request.FILES to handle file uploads
        form = TourPackageForm(request.POST, request.FILES)
        if form.is_valid():
            package = form.save(commit=False)
            package.provider = request.user  # Assign the logged-in user as the provider
            package.save()
            return redirect('package_list')  # Redirect to the package list page after saving
    else:
        form = TourPackageForm()
    
    return render(request, 'add_package.html', {'form': form})



# @login_required
# def package_list(request):
#     packages = TourPackage.objects.filter(provider=request.user)
#     return render(request, 'package_list.html', {'packages': packages})
@login_required
def package_list(request):
    if request.user.is_staff:  # Admins can see all packages
        packages = TourPackage.objects.all()
    else:  # Providers only see their own packages
        packages = TourPackage.objects.filter(provider=request.user)
    
    return render(request, 'package_list.html', {'packages': packages})

def packagelist(request):
    packages = TourPackage.objects.filter(verified=True, availability=True)
    return render(request, 'packagelist.html', {'packages': packages})

from django.shortcuts import render, redirect
from .models import TourPackage
from django.http import Http404

@login_required
def remove_package(request, package_id):
    # Get the package based on the provided ID
    try:
        package = TourPackage.objects.get(id=package_id)
    except TourPackage.DoesNotExist:
        raise Http404("Package not found")

    # Remove the package from the database
    if request.method == "POST":
        package.delete()
        return redirect('package_list')  # Redirect to the packages list page

    return redirect('package_list')  # Redirect to the packages list page if not POST request

@login_required
def edit_package(request, package_id):
    package = get_object_or_404(TourPackage, id=package_id)
    
    if request.method == 'POST':
        form = TourPackageForm(request.POST, request.FILES, instance=package)
        if form.is_valid():
            form.save()
            return redirect('package_list')
    else:
        form = TourPackageForm(instance=package)
    
    return render(request, 'edit_package.html', {'form': form, 'package': package})


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import TourPackage, Booking
from .forms import BookingForm  # Import the form


def packagelist(request):
    packages = TourPackage.objects.filter(verified=True, availability=True)
    return render(request, 'packagelist.html', {'packages': packages})


# def packagelist(request):
#     packages = TourPackage.objects.all()  # Ensure packages exist
#     return render(request, 'packagelist.html', {'packages': packages})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import TourPackage, Booking
from django.contrib import messages
from datetime import datetime

import razorpay
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .models import TourPackage, Booking, Payment

# Initialize Razorpay Client
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

@login_required
def book_package(request, package_id):
    package = get_object_or_404(TourPackage, id=package_id)

    # Check if the user has already booked this package
    # if Booking.objects.filter(user=request.user, package=package).exists():
    #     messages.error(request, "You have already booked this package.")
    #     return redirect('userdash')  

    if request.method == 'POST':
        number_of_people = int(request.POST.get('number_of_people', 1))

        if number_of_people < 1 or number_of_people > 10:
            messages.error(request, "You can only book for 1 to 10 people.")
            return render(request, 'book_packages.html', {'package': package})

        booking_date_str = request.POST.get('booking_date')
        try:
            booking_date = datetime.strptime(booking_date_str, "%Y-%m-%d").date()
            if booking_date < datetime.today().date():
                messages.error(request, "Booking date cannot be in the past.")
                return render(request, 'book_packages.html', {'package': package})
        except (ValueError, TypeError):
            messages.error(request, "Invalid date format. Please select a valid date.")
            return render(request, 'book_packages.html', {'package': package})

        # Calculate total price
        total_price = int(package.price * number_of_people * 100) # Convert to paisa (Razorpay expects amount in paisa)

        # Create Razorpay Order
        order_data = {
            "amount": total_price,
            "currency": "INR",
            "payment_capture": "1"  # Auto-capture payment
        }
        razorpay_order = razorpay_client.order.create(data=order_data)
        

        # Store booking details temporarily (optional: use session or DB)
        request.session['booking_data'] = {
            'package_id': package.id,
            'number_of_people': number_of_people,
            'booking_date': booking_date_str,
            'razorpay_order_id': razorpay_order['id']
        }

        # Render payment page
        context = {
            'package': package,
            'razorpay_order_id': razorpay_order['id'],
            'razorpay_key': settings.RAZORPAY_KEY_ID,
            'total_price': total_price / 100,  # Convert back to INR
        }
        return render(request, 'payment.html', context)

    return render(request, 'book_packages.html', {'package': package})


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, get_object_or_404


@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        razorpay_order_id = request.POST.get("razorpay_order_id")
        payment_id = request.POST.get("razorpay_payment_id")
        signature = request.POST.get("razorpay_signature")

        try:
            # Verify the payment signature
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            result = razorpay_client.utility.verify_payment_signature(params_dict)

            if result:
                booking_data = request.session.get('booking_data')
                if booking_data:
                    package = get_object_or_404(TourPackage, id=booking_data['package_id'])

                    # Create Booking
                    booking = Booking.objects.create(
                        user=request.user,
                        package=package,
                        number_of_people=booking_data['number_of_people'],
                        booking_date=datetime.strptime(booking_data['booking_date'], "%Y-%m-%d").date()
                    )

                    # Save Payment
                    Payment.objects.create(
                        booking=booking,
                        razorpay_order_id=razorpay_order_id,
                        razorpay_payment_id=payment_id,
                        amount=package.price * booking.number_of_people
                    )

                    del request.session['booking_data']  # Clear session

                    messages.success(request, f"Your booking for {package.title} has been confirmed!")
                    return redirect('userdash')
                else:
                    messages.error(request, "Session expired! Please try booking again.")
                    return redirect('book_package', package_id=package.id)
        except Exception as e:
            messages.error(request, f"Payment verification failed: {str(e)}")
            return redirect('userdash')

    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'my_bookings.html', {'bookings': bookings})


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Booking, TourPackage

@login_required
def userdash(request):
    user = request.user
    bookings = Booking.objects.filter(user=user)
    available_packages = TourPackage.objects.exclude(id__in=bookings.values_list('package_id', flat=True))

    return render(request, 'userdash.html', {
        'user': user,
        'bookings': bookings,
        'available_packages': available_packages
    })

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Booking

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if request.method == 'POST':
        booking.delete()
        messages.success(request, "Your booking has been successfully canceled.")
        return redirect('userdash')  # Redirect to the user's bookings page

    return render(request, 'cancel_package.html', {'booking': booking})



