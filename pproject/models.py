from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from pproject import validators


class CarConstants:
    CAR_TYPE_CHOICES = (
        (u'', u'Transport type'),
        ("t1", ("type1")),
        ("t2", ("type2")),
    )
    FUEL_CHOICES = (
        (u'', u'Fuel type'),
        ("t1", ("type1")),
        ("t2", ("type2")),
    )
    TRANSMISSION_CHOICES = (
        (u'', u'Transmission type'),
        ("t1", ("type1")),
        ("t2", ("type2")),
    )
    CONDITION_CHOICES = (
        (u'', u'Condition'),
        ("t1", ("type1")),
        ("t2", ("type2")),
    )


class CommonUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(
        validators=[validators.validate_date_of_birth],
        null=False,
        blank=False)
    city = models.CharField(max_length=60, null=True, blank=True)
    phone = models.IntegerField(null=True, blank=True)
    vk = models.CharField(max_length=60, null=True, blank=True)
    fb = models.CharField(max_length=60, null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    photo = models.ImageField(
        upload_to='img/users_avatars/',
        default='img/users_avatars/default.jpg')

    docs_are_checked = models.BooleanField(default=False)
    soc_networks_are_checked = models.BooleanField(default=False)
    # TODO: develop rating system, it's could be \
    # model method or model field
    # rating = models.PositiveIntegerField()

    def __unicode__(self):
        return u"%s %s" % (self.user.first_name, self.user.last_name)


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
    photo = models.ImageField(
        upload_to='img/users_cars_photos/',
        default='img/users_cars_photos/car.jpg',
        null=False,
        blank=False)
    price = models.PositiveIntegerField()
    description_title = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    rental_perion_begin = models.DateTimeField(
        validators=[validators.validate_rental_perion_begin])
    rental_perion_end = models.DateTimeField(
        validators=[validators.validate_rental_perion_end])
    country = models.CharField(
        null=True,
        blank=False,
        max_length=100)
    city = models.CharField(
        null=True,
        blank=False,
        max_length=100)
    street = models.CharField(
        null=True,
        blank=False,
        max_length=100)
    building = models.PositiveIntegerField(
        null=True,
        blank=False)
    docs = models.FileField(
        upload_to='car_docs/',
        null=True,
        blank=True)
    is_insured = models.BooleanField(default=False)
    owner = models.ForeignKey(
        CommonUser,
        related_name='user_own_cars',
        null=True,
        blank=True)
    renter = models.ForeignKey(
        CommonUser,
        related_name='user_rent_cars',
        null=True,
        blank=True)

    def rental_period(self):
        rental_perion = self.rental_perion_end - self.rental_perion_begin
        return rental_perion

    def __unicode__(self):
        rental_period = Car.rental_period(self)
        return u"%s, %s. Price: %d, yet there are (%s) in rent" % (
            self.model, self.transmission, self.price, rental_period)
