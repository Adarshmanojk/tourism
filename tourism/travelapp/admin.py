from django.contrib import admin
from travelapp.models import Flights,Hotels,City,BookFlight,BookHotel,BookPackage,Famous,TourPackage,Booking,Payment,ContactMessage,provider

# Register your models here.
admin.site.register(Flights)
admin.site.register(Hotels)
admin.site.register(City)
# admin.site.register(BookFlight)
# admin.site.register(BookHotel)
admin.site.register(ContactMessage)
admin.site.register(Famous)
admin.site.register(provider)
# admin.site.register(TourProviderUser)
# admin.site.register(TourPackage)
admin.site.register(Booking)
admin.site.register(Payment)
# @admin.register(ContactMessage)

# Register your models here.

@admin.register(TourPackage)
class TourPackageAdmin(admin.ModelAdmin):
    list_display = ('title', 'provider', 'price', 'verified', 'availability')
    list_filter = ('verified', 'availability')
    actions = ['mark_as_verified']

    def mark_as_verified(self, request, queryset):
        queryset.update(verified=True)
    mark_as_verified.short_description = "Mark selected packages as verified"

@admin.register(BookFlight)
class BookFlightAdmin(admin.ModelAdmin):
    pass

@admin.register(BookHotel)
class BookHotelAdmin(admin.ModelAdmin):
    pass

@admin.register(BookPackage)
class BookPackageAdmin(admin.ModelAdmin):
    pass
class MyModelAdmin(admin.ModelAdmin):
    class Media:
        css = {
            "all": ("custom_admin.css",),
        }
