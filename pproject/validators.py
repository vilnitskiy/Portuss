from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError


def validate_rental_perion_begin(value):
    if value < timezone.now():
        raise ValidationError(
            "You can start to rent your car only from present date!")
    return "OK"


def validate_rental_perion_end(value):
    if value > timezone.now() + relativedelta(days=365):
        raise ValidationError(
            "You can't rent car more than 365 days long!")
    elif value <= timezone.now():
        raise ValidationError(
            "Please, enter the future date!")
    return "OK"


def validate_date_of_birth(value):
    #if value > timezone.now():
    #    raise ValidationError("Please, write your real date of birth!")
    return "OK"


def validate_price(value):
    if value % 100 == 0:
        return "OK"
    else:
        raise ValidationError(
            "Please, write the price divisible by 100")
