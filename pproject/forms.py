from django.forms import ModelForm
from pproject.models import Car


class CarRentForm1(ModelForm):
    class Meta:
        model = Car
        fields = (
            'car_type', 'fuel', 'transmission',
            'issue_date', 'condition', 'mileage',
            'model')


class CarRentForm2(ModelForm):
    class Meta:
        model = Car
        fields = ('photos',)


class CarRentForm3(ModelForm):
    class Meta:
        model = Car
        fields = ('car-rent-title', 'car-rent-description')
