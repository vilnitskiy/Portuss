# -*- coding: utf-8 -*-
from datetime import date
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

from pproject import validators


class CommonUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(
        validators=[validators.validate_date_of_birth],
        null=True,
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
    comment = models.TextField(null=True, blank=True)
    user_rating = models.PositiveIntegerField(
        default=3,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)])

    def __unicode__(self):
        return u"%s %s" % (self.user.first_name, self.user.last_name)


class CarType(models.Model):
    _car = models.CharField(
        max_length=30)

    def __unicode__(self):
        return u"%s" % (self._car)


class FuelType(models.Model):
    _fuel = models.CharField(
        max_length=30)

    def __unicode__(self):
        return u"%s" % (self._fuel)


class TrasmissionType(models.Model):
    _transmission = models.CharField(
        max_length=30)

    def __unicode__(self):
        return u"%s" % (self._transmission)


class ConditionType(models.Model):
    _condition = models.CharField(
        max_length=30)

    def __unicode__(self):
        return u"%s" % (self._condition)


class Car(models.Model):
    car_type = models.ForeignKey(CarType)
    fuel = models.ForeignKey(FuelType)
    transmission = models.ForeignKey(TrasmissionType)
    issue_date = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1950),
            MaxValueValidator(date.today().year)])
    condition = models.ForeignKey(ConditionType)
    # mileage in thousands of km
    mileage = models.PositiveIntegerField(
        validators=[MaxValueValidator(300)])
    model = models.CharField(max_length=10)
    photo = models.FileField(
        upload_to='img/users_cars_photos/',
        default='img/users_cars_photos/car.jpg',
        null=True,
        blank=True)
    price = models.PositiveIntegerField(
        default=200,
        blank=False,
        validators=[validators.validate_price,
                    MinValueValidator(100),
                    MaxValueValidator(10000)])
    description_title = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    rental_perion_begin = models.DateField(
        default=datetime.now,
        blank=False)
    rental_perion_end = models.DateField(
        default=datetime.now,
        blank=False)
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
    __original_renter = None
    times_rented = models.PositiveIntegerField(
        default=0,
        blank=True,
        null=False)
    car_rating = models.PositiveIntegerField(
        default=3,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)])

    def rental_period(self):
        rental_perion = self.rental_perion_end - self.rental_perion_begin
        return rental_perion

    def __init__(self, *args, **kwargs):
        super(Car, self).__init__(*args, **kwargs)
        self.__original_renter = self.renter

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        if self.renter != self.__original_renter:
            self.times_rented += 1
        super(Car, self).save(force_insert, force_update, *args, **kwargs)
        self.__original_renter = self.renter

    def __unicode__(self):
        rental_period = Car.rental_period(self)
        return u"%s, %s. Price: %d, yet there are (%s) in rent" % (
            self.model, self.transmission, self.price, rental_period)


class CommentCarOwner(models.Model):
    comment_body = models.TextField(null=True, blank=True)
    comment_date = models.DateField(
        default=datetime.now,
        blank=False)
    is_interesting = models.PositiveIntegerField(
        default=0,
        blank=True,
        null=False)
    comment_author = models.ForeignKey(
        CommonUser,
        related_name='comment_author',
        null=False,
        blank=False)
    commented_user = models.ForeignKey(
        CommonUser,
        related_name='commented_user',
        null=False,
        blank=False)

    def __unicode__(self):
        return u"Comment for %s, %s" % (
            self.commented_user.user.first_name,
            self.commented_user.user.last_name)


class CommentCar(models.Model):
    comment_body = models.TextField(
        null=False,
        blank=False,
        default='comment')
    comment_date = models.DateField(
        default=datetime.now,
        blank=False)
    is_interesting = models.PositiveIntegerField(
        default=0,
        blank=True,
        null=False)
    comment_author = models.ForeignKey(
        CommonUser,
        related_name='comment_car_author',
        null=True,
        blank=True)
    commented_car = models.ForeignKey(
        Car,
        related_name='commented_car',
        null=False,
        blank=False)
    unauthed_user_email = models.EmailField(
        null=True,
        blank=True)

    def __unicode__(self):
        return u"Comment for %s" % (self.commented_car)
