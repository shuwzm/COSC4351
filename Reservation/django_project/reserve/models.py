from django.db import models
from django.db.models.fields import DateTimeField, NullBooleanField
from django.db.models.fields.related import ForeignKey
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from table.models import Table

# Create your models here.

class Reservation(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = PhoneNumberField(null=False, blank=True, unique=False, region="US")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    table_id = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='table_id')
    table2nd_id = models.ForeignKey(Table, on_delete=models.CASCADE, null=True, related_name='table2nd_id')
    date = models.DateField()
    arrive = models.TimeField()
    duration = models.DurationField()
    come = models.DateTimeField(null=True)
    out = models.DateTimeField(null=True)
    customer_number = models.IntegerField(default=0)
    is_expired = models.BooleanField(default=True)
    has_come = models.BooleanField(default=False)

class HighTrafficDay(models.Model):
    date = models.DateField()