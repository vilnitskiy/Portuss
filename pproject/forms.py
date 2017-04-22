from random import choice
from string import letters
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django import forms

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
            'email',
            'password1', 'password2',
            'first_name', 'last_name',)

    def save(self):
        random = ''.join([choice(letters) for i in xrange(30)])
        self.instance.username = random
        return super(BaseUserForm, self).save()


class UserRegistrationForm(ModelForm):
    class Meta:
        model = CommonUser
        exclude = ['user', 'own_cars', 'tenant_cars']


class RegistrationMultiForm(MultiModelForm):
    form_classes = {
        'base_user': BaseUserForm,
        'common_user': UserRegistrationForm,
    }


class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = (
            'email', 'password',)
        widgets = {
            'password': forms.PasswordInput(),
        }

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget = forms.TextInput(attrs={
            'id': 'login-e-mail'})
        self.fields['password'].widget = forms.PasswordInput(attrs={
            'id': 'login-password'})

    def clean(self):
        username = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError(
                "Something went wrong, check your email and password and try again")
        return self.cleaned_data
