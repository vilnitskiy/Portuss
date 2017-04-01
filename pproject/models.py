from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from pproject import validators


class CarConstants:
    CAR_TYPE_CHOICES = (
        ("t1", ("type1")),
        ("t2", ("type2")),
    )
    FUEL_CHOICES = (
        ("t1", ("type1")),
        ("t2", ("type2")),
    )
    TRANSMISSION_CHOICES = (
        ("t1", ("type1")),
        ("t2", ("type2")),
    )
    CONDITION_CHOICES = (
        ("t1", ("type1")),
        ("t2", ("type2")),
    )


class Car(models.Model):
    car_type = models.CharField(
        choices=CarConstants.CAR_TYPE_CHOICES,
        max_length=30)
    fuel = models.CharField(
        choices=CarConstants.FUEL_CHOICES,
        max_length=30)
    transmission = models.CharField(
        choices=CarConstants.TRANSMISSION_CHOICES,
        max_length=30)
    issue_date = models.DateField()
    condition = models.CharField(
        choices=CarConstants.CONDITION_CHOICES,
        max_length=20)
    mileage = models.PositiveIntegerField()
    model = models.CharField(max_length=10)
    photos = models.ImageField()
    price = models.PositiveIntegerField()
    description_title = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    rental_perion_begin = models.DateTimeField(
        validators=[validators.validate_rental_perion_begin])
    rental_perion_end = models.DateTimeField(
        validators=[validators.validate_rental_perion_end])

    @staticmethod
    def rental_period(self):
        rental_perion = self.rental_perion_end - self.rental_perion_begin
        return rental_perion

    def __unicode__(self):
        rental_period = Car.rental_period(self)
        return u"%s, %s. Price: %d, yet there are (%s) in rent" % (
            self.model, self.transmission, self.price, rental_period)


class CommonUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    own_cars = models.ForeignKey(Car, related_name='user_own_cars')
    tenant_cars = models.ForeignKey(Car, related_name='user_tenant_cars')
    # TODO: develop rating system, it's could be \
    # model method or model field
    # rating = models.PositiveIntegerField()

    def __unicode__(self):
        return u"%s %s" % (self.user.first_name, self.user.last_name)
