import json

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views import View
from django.views.generic.edit import CreateView
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.contrib.auth.models import User
from django import forms

from pproject.models import CommonUser
from pproject.forms import CarRentForm1, CarRentForm2, CarRentForm3, \
    RegistrationMultiForm, LoginForm


def main(request):
    form = LoginForm
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            new_user = authenticate(username=form.cleaned_data['email'],
                                    password=form.cleaned_data['password'])
            login(request, new_user)
    return render(request, 'main.html', {'form': form})


class RegistrationView(CreateView):
    form_class = RegistrationMultiForm
    template_name = 'registration/registration.html'
    success_url = 'main'

    def form_valid(self, form):
        user = form['base_user'].save()
        common_user = form['common_user'].save(commit=False)
        common_user.user = User.objects.get(username=user.username)
        common_user.save()
        try:
            new_user = authenticate(
                username=form['base_user'].cleaned_data['email'],
                password=form['base_user'].cleaned_data['password1'])
            login(self.request, new_user)
        except:
            raise forms.ValidationError(
                "Error!")
        return redirect(reverse(self.success_url))


class CarRentView(View):
    form_class = CarRentForm1
    template_name = 'set_car_rent.html'

    def get(self, request, *args, **kwargs):
        form1 = self.form_class()
        return render(request, self.template_name, {'form1': form1})

    def post(self, request, *args, **kwargs):
        form1 = self.form_class(request.POST)
        if form1.is_valid():
            return HttpResponse()
        else:
            json_data = json.dumps(form1.errors)
            return HttpResponse(
                json_data, {'content_type': 'application/json'})
        return render(request, self.template_name, {'form1': form1})
