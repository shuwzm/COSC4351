from django.contrib import admin

# Register your models here.
from .models import Reservation
from .models import HighTrafficDay

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'table_id', 'table2nd_id', 'customer_number')
admin.site.register(Reservation, ReservationAdmin)

class HighTrafficDayAdmin(admin.ModelAdmin):
    list_display = ('id','date')
admin.site.register(HighTrafficDay, HighTrafficDayAdmin)