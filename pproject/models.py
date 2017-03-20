from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Car(models.Model):
    car_type = models.CharField(max_length=20)
    fuel = models.CharField(max_length=10)
    transmission = models.CharField(max_length=10)
    issue_date = models.DateField()
    condition = models.CharField(max_length=20)
    mileage = models.PositiveIntegerField()
    model = models.CharField(max_length=10)
    photos = models.ImageField()
    price = models.PositiveIntegerField()
    description = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(User)
    tenant = models.ForeignKey(User)
    rental_perion_begin = models.DateTimeField()
    rental_perion_end = models.DateTimeField()

    def __unicode__(self):
        return u"%s - %s" % (self.model, self.owner)
