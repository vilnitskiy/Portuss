from random import choice
from string import letters
from django.forms import ModelForm, Form
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django import forms

from betterforms.multiform import MultiModelForm

from pproject.models import Car, CommonUser,\
    CommentCarOwner, CommentCar


class CarRentForm1(ModelForm):
    class Meta:
        model = Car
        fields = (
            'car_type', 'fuel', 'transmission',
            'issue_date', 'condition', 'mileage',
            'model', 'country', 'city', 'street',
            'building',)

    def __init__(self, *args, **kwargs):
        super(CarRentForm1, self).__init__(*args, **kwargs)
        self.fields['car_type'].widget.attrs.update({
            'id': 'transport-type'})
        self.fields['fuel'].widget.attrs.update({
            'id': 'fuel-type'})
        self.fields['transmission'].widget.attrs.update({
            'id': 'transmission-type'})
        self.fields['issue_date'].widget.attrs.update({
            'id': 'manufactured-year', 'placeholder': 'Year of manufacturing'})
        self.fields['condition'].widget.attrs.update({
            'id': 'condition'})
        self.fields['mileage'].widget.attrs.update({
            'id': 'mileage', 'placeholder': 'Mileage'})
        self.fields['model'].widget.attrs.update({
            'placeholder': 'Brand/Model'})
        self.fields['country'].widget.attrs.update({
            'id': 'car-country', 'placeholder': 'Country'})
        self.fields['city'].widget.attrs.update({
            'id': 'car-city', 'placeholder': 'City'})
        self.fields['street'].widget.attrs.update({
            'id': 'car-street', 'placeholder': 'Steet'})
        self.fields['building'].widget.attrs.update({
            'id': 'car-house', 'placeholder': 'Building'})


class CarRentForm2(ModelForm):
    class Meta:
        model = Car
        fields = ('photo',)

    def __init__(self, *args, **kwargs):
        super(CarRentForm2, self).__init__(*args, **kwargs)
        self.fields['photo'].widget.attrs.update({
            'id': 'car-gallery-load'})


class CarRentForm3(ModelForm):
    class Meta:
        model = Car
        fields = ('description_title', 'description',)

    def __init__(self, *args, **kwargs):
        super(CarRentForm3, self).__init__(*args, **kwargs)
        self.fields['description_title'].widget.attrs.update({
            'id': 'car-card-heading', 'rows': '2',
            'placeholder': 'Here you can write'
            'the title for the ad, otherwise'
            'the system will generate it yourself.'})
        self.fields['description'].widget.attrs.update({
            'id': 'car-card-description',
            'placeholder': 'Here you can describe all'
            'the nuances: the rules of behavior in'
            'the car, whether it is possible to smoke'
            'inside, whether the tank will be filled when'
            'renting, etc.'})


class CarRentForm4(ModelForm):
    class Meta:
        model = Car
        fields = ('rental_perion_begin', 'rental_perion_end', 'price',)

    def __init__(self, *args, **kwargs):
        super(CarRentForm4, self).__init__(*args, **kwargs)
        self.fields['rental_perion_begin'].widget.attrs.update({
            'id': 'rent-terms-from',
            'placeholder': 'from',
            'class': 'hasDatepicker'})
        self.fields['rental_perion_end'].widget.attrs.update({
            'id': 'rent-terms-to',
            'placeholder': 'to',
            'class': 'hasDatepicker'})
        self.fields['price'].widget.attrs.update({
            'id': 'form-price',
            'placeholder': 'Enter the price'})


class CarRentForm5(ModelForm):
    class Meta:
        model = Car
        fields = ('docs', 'is_insured',)

    def __init__(self, *args, **kwargs):
        super(CarRentForm5, self).__init__(*args, **kwargs)
        self.fields['docs'].widget.attrs.update({
            'id': 'car-document-load'})
        self.fields['is_insured'].widget.attrs.update({
            'id': 'car-insurance'})


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


class QuickSearchForm(Form):
    city = forms.CharField(max_length=60)
    rental_perion_begin = forms.DateField()
    rental_perion_end = forms.DateField()

    def __init__(self, *args, **kwargs):
        super(QuickSearchForm, self).__init__(*args, **kwargs)
        self.fields['city'].widget = forms.TextInput(attrs={
            'placeholder': 'City'})
        self.fields['rental_perion_begin'].widget = forms.TextInput(attrs={
            'id': 'page-search-date-from',
            'placeholder': 'from'})
        self.fields['rental_perion_end'].widget = forms.TextInput(attrs={
            'id': 'page-search-date-to',
            'placeholder': 'to'})

    def clean(self):
        r_begin = self.cleaned_data.get('rental_perion_begin')
        r_end = self.cleaned_data.get('rental_perion_end')
        if (r_end - r_begin).days > 365:
            raise forms.ValidationError(
                "You can't rent car for more than year.")
        return self.cleaned_data


class SearchForm(CarRentForm1, QuickSearchForm):
    myear1 = forms.IntegerField()
    myear2 = forms.IntegerField()
    mileage1 = forms.IntegerField()
    mileage2 = forms.IntegerField()
    price1 = forms.IntegerField()
    price2 = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields['mileage1'].widget = forms.TextInput(attrs={
            'placeholder': 'from'})
        self.fields['mileage2'].widget = forms.TextInput(attrs={
            'placeholder': 'to'})
        self.fields['price1'].widget = forms.TextInput(attrs={
            'placeholder': 'from'})
        self.fields['price2'].widget = forms.TextInput(attrs={
            'placeholder': 'to'})
        self.fields['model'].widget = forms.TextInput(attrs={
            'id': 'brand',
            'placeholder': 'Brand/Model'})
        self.fields['myear1'].widget = forms.TextInput(attrs={
            'placeholder': 'from'})
        self.fields['myear2'].widget = forms.TextInput(attrs={
            'placeholder': 'to'})


class BaseEditUserForm(ModelForm):
    class Meta:
        model = User
        fields = (
            'email',
            'first_name', 'last_name',)


class UserEditForm(ModelForm):
    class Meta:
        model = CommonUser
        exclude = ['user', 'own_cars', 'tenant_cars', 'photo']


class EditMultiForm(MultiModelForm):
    form_classes = {
        'base_user': BaseEditUserForm,
        'common_user': UserEditForm,
    }

    def __init__(self, *args, **kwargs):
        super(EditMultiForm, self).__init__(*args, **kwargs)
        for key1 in self['base_user'].fields:
            if key1 != 'password':
                self['base_user'].fields[key1].required = False

        for key2 in self['common_user'].fields:
            self['common_user'].fields[key2].required = False


class CommentCarOwnerForm(ModelForm):
    class Meta:
        model = CommentCarOwner
        fields = ('comment_body',)


class CommentCarForm(ModelForm):
    class Meta:
        model = CommentCar
        fields = ('comment_body', 'unauthed_user_email',)
