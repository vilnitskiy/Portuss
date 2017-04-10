from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from betterforms.multiform import MultiModelForm

from pproject.models import Car, CommonUser


class CarRentForm1(ModelForm):
    class Meta:
        model = Car
        fields = (
            'car_type', 'fuel', 'transmission',
            'issue_date', 'condition', 'mileage',
            'model',)


class CarRentForm2(ModelForm):
    class Meta:
        model = Car
        fields = ('photos',)


class CarRentForm3(ModelForm):
    class Meta:
        model = Car
        fields = ('description_title', 'description',)


class BaseUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'email', 'username',
            'password1', 'password2',
            'first_name', 'last_name',)


class UserRegistrationForm(ModelForm):
    class Meta:
        model = CommonUser
        exclude = ['user', 'own_cars', 'tenant_cars']


class RegistrationMultiForm(MultiModelForm):
    form_classes = {
        'base_user': BaseUserForm,
        'common_user': UserRegistrationForm,
    }
