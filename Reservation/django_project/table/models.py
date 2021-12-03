from django.db import models

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Table(models.Model):
    tableId = models.CharField(max_length=100)
    capacity = models.IntegerField()
    isOutdoor = models.BooleanField(default=False)
    isBooth = models.BooleanField(default=False)
    isCurAvailable = models.BooleanField(default=True)

    def __str__(self):
        return self.tableId

    def get_absolute_url(self):
        return reverse('table-home')
