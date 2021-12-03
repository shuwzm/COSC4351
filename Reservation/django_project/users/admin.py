import address
from django.contrib import admin
from django.contrib.auth.models import User
from address.models import Country
from address.models import Locality
from address.models import State
from address.models import Address

# Register your models here.
from .models import Profile

admin.site.register(Profile)

admin.site.unregister(Country)
admin.site.unregister(Locality)
admin.site.unregister(State)
admin.site.unregister(Address)