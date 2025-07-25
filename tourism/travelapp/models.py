from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.apps import apps  # Import Flights model
from datetime import date
from django.utils import timezone
# Create your models here.

class City(models.Model):
    city = models.CharField(max_length=200)
    bestlink = models.CharField(max_length=200)
    weekgetlinks = models.CharField(max_length=200)

    def __str__(self):
        return self.city

class Flights(models.Model):
    id = models.AutoField(primary_key=True)
    source = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    flight_num = models.CharField(max_length=10, unique=True)  # Ensuring unique flight numbers
    city = models.ForeignKey(City, on_delete=models.CASCADE)  # ✅ Added City back
    
    eprice = models.IntegerField(default=0, null=True, blank=True)  # Economy price
    bprice = models.IntegerField(default=0, null=True, blank=True)  # Business price
    
    economy_seats = models.IntegerField(default=0)  # Total economy seats
    business_seats = models.IntegerField(default=0)  # Total business seats

    dept_time = models.TimeField()
    dest_time = models.TimeField()
    company = models.CharField(max_length=15, default=" ")

    def __str__(self):
        return f"{self.company} {self.flight_num}"

    def available_seats(self, date, seat_class):
        """
        Returns the number of available seats for a given date and seat class.
        """
        booked_seats = BookFlight.objects.filter(
            flight=self.flight_num, 
            date=date, 
            seat_class=seat_class
        ).aggregate(total=models.Sum('seat'))['total'] or 0  # Default to 0 if no bookings exist

        return self.economy_seats - booked_seats if seat_class == "economy" else self.business_seats - booked_seats



class BookFlight(models.Model):
    username_id = models.ForeignKey(User, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flights, on_delete=models.CASCADE)  # ✅ Change to ForeignKey
    date = models.DateField()  
    seat = models.IntegerField(default=1)
    
    seat_class = models.CharField(
        max_length=10,
        choices=[('economy', 'Economy'), ('business', 'Business')],
        default='economy'  
    )
    total_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[("pending", "Pending"), ("confirmed", "Confirmed")],
        default="Confirmed"
    )

    def save(self, *args, **kwargs):
        if self.flight:  # ✅ No need to query Flights manually
            if self.seat_class == "economy":
                self.total_price = self.seat * self.flight.eprice
            elif self.seat_class == "business":
                self.total_price = self.seat * self.flight.bprice

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username_id} - {self.flight.flight_num} ({self.seat_class})"



class Hotels(models.Model):
    id = models.AutoField(primary_key=True)
    city = models.ForeignKey(City,on_delete=models.CASCADE)
    hotel_name = models.CharField(max_length=200)
    hotel_address = models.CharField(max_length=500)
    hotel_price = models.IntegerField(null=True)
    hotel_rating = models.IntegerField(null=True)
    amenities = models.CharField(max_length=500)
    distfromap = models.IntegerField(null=True)
    rooms = models.IntegerField(default=0)
    image1 = models.ImageField(null=True,upload_to='img/')


    def __str__(self):
        return self.hotel_name



class BookHotel(models.Model):
    username_id = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel_name = models.ForeignKey(Hotels, on_delete=models.CASCADE)  # FK instead of CharField
    date = models.DateField()
    room = models.IntegerField(default=1)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[("pending", "Pending"), ("confirmed", "Confirmed")],
        default="Confirmed"
    )

    def save(self, *args, **kwargs):
        if self.hotel_name:  # Ensure hotel exists
            self.total_price = self.room * self.hotel_name.hotel_price  # Using your formula
        super(BookHotel, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.hotel_name} - {self.date} - {self.username_id.username}"


class BookPackage(models.Model):
    username_id = models.ForeignKey(User, on_delete=models.CASCADE)
    seat = models.IntegerField(default=1)
    flight = models.ForeignKey(Flights, on_delete=models.CASCADE)  # FK to Flights model
    hotel_name = models.ForeignKey(Hotels, on_delete=models.CASCADE)  # FK to Hotels model
    room = models.IntegerField(default=1)
    
    # Changed to 'seat_class' for flight seat class selection
    seat_class = models.CharField(
        max_length=10,
        choices=[('economy', 'Economy'), ('business', 'Business')],
        default='economy'
    )
    
    date = models.DateField()  # Changed to DateField for better date handling
    total_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[("pending", "Pending"), ("confirmed", "Confirmed")],
        default="Confirmed"
    )

    def save(self, *args, **kwargs):
        # Automatically calculate the total price for the package
        if self.flight and self.hotel_name:
            flight_obj = Flights.objects.get(flight_num=self.flight.flight_num)
            hotel_obj = Hotels.objects.get(id=self.hotel_name.id)

            # Calculate total price based on seat class
            if self.seat_class == 'economy':
                flight_price = self.seat * flight_obj.eprice
            else:
                flight_price = self.seat * flight_obj.bprice

            # For hotel, you can adjust this if you want to change pricing based on room type or class
            hotel_price = self.room * hotel_obj.hotel_price  # Assuming the same price for the hotel room

            self.total_price = flight_price + hotel_price

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Package for {self.username_id.username} - Flight: {self.flight} ({self.seat_class}) and Hotel: {self.hotel_name}"


    
class Famous(models.Model):
    city = models.ForeignKey(City,on_delete=models.CASCADE)
    place_name = models.CharField(max_length=200)
    image = models.ImageField(null=True,upload_to='img/')
    desc = models.CharField(max_length=500)

    def __str__(self):
        return self.place_name
    

from django.db.models import Q
# Create your models here.


class provider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="provider_profile")
    name=models.CharField(max_length=100)
    phone=models.CharField(max_length=20)
    email=models.EmailField()
    username=models.CharField(max_length=50)
    password=models.CharField(max_length=50)

    def __str__(self):
        return self.username

from django.db import models
from django.conf import settings

class TourPackage(models.Model):
    provider = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="packages"
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    availability = models.PositiveIntegerField()  # Number of available slots
    duration = models.CharField(max_length=100, null=True, blank=True)
  # Example: '3 days, 2 nights'
    image = models.ImageField(upload_to='img/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)  # New field for admin verification

    def __str__(self):
        return self.title


from django.db import models
from django.conf import settings
from .models import TourPackage

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings")
    package = models.ForeignKey(TourPackage, on_delete=models.CASCADE, related_name="bookings")
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[("pending", "Pending"), ("confirmed", "Confirmed")], default="Confirmed")
    number_of_people = models.PositiveIntegerField(default=1)  # How many people are booking for the tour
    booking_date = models.DateField() 
    total_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.total_price = self.package.price * self.number_of_people  # Calculate total price based on number of people
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking by {self.user.username} for {self.package.title}"
    

class Payment(models.Model):
    # booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, null=True, blank=True)

    razorpay_order_id = models.CharField(max_length=100, unique=True)
    # razorpay_payment_id = models.CharField(max_length=100, unique=True)
    razorpay_payment_id = models.CharField(max_length=100, unique=True, default="default_payment_id")

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.razorpay_payment_id} for {self.booking}"

from django.contrib.auth.models import User

class ContactMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    reply = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    replied_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.email}"
