from django.contrib import admin

# Register your models here.

from .models import Table


admin.site.register (Table)

admin.site.site_header = 'Reservation System Administration'