import json

from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
from django.views.generic.edit import CreateView
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django import forms
from django.conf import settings

from pproject.models import CommonUser, Car
from pproject.forms import CarRentForm1, CarRentForm2, CarRentForm3, \
    CarRentForm4, CarRentForm5, RegistrationMultiForm, LoginForm


def main(request):
    form = LoginForm
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            new_user = authenticate(username=form.cleaned_data['email'],
                                    password=form.cleaned_data['password'])
            login(request, new_user)
    if (request.user.is_authenticated() and
            not request.user.is_superuser and
            not request.user.is_staff):
        base_user = User.objects.get(username=request.user.username)
        user = CommonUser.objects.get(user=base_user)
    elif request.user.is_superuser or request.user.is_staff:
        user = User.objects.get(username=request.user.username)
    else:
        user = ''
    return render(request, 'main.html', {'form': form, 'common_user': user})


class RegistrationView(CreateView):
    form_class = RegistrationMultiForm
    template_name = 'registration/registration.html'
    success_url = 'main'

    def form_valid(self, form):
        user = form['base_user'].save()

        common_user = form['common_user'].save(commit=False)
        common_user.user = User.objects.get(username=user.username)
        common_user.save()
        new_user = authenticate(
            username=form['base_user'].cleaned_data['email'],
            password=form['base_user'].cleaned_data['password1'])
        login(self.request, new_user)

        return redirect(reverse(self.success_url))


class CarRentView(FormView):
    """
    How it works.

    First we pass CarRentForm1 rendered to html to js via ajax,
    after that we get next_form parameter from js and render next
    form and get it in js
    """

    form_class = CarRentForm1
    form_classes = [
        CarRentForm1, CarRentForm2,
        CarRentForm3, CarRentForm4,
        CarRentForm5]
    template_name = 'set_car_rent.html'

    def get(self, request, *args, **kwargs):
        form1 = self.form_class()
        if request.is_ajax():
            return HttpResponse(form1)
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        """
        Form post.

        Post current form and prepare the next one for loading via js.
        As it could return either next form of current form errors,
        form errors updates by special marker to differentiate form
        from form errors

        """
        if request.is_ajax():
            next_step = int(request.POST['next_step'])
            next_form_class = next_rent_form_class(next_step)
            val_form = self.form_classes[next_step - 1]
            submited_form = val_form(request.POST)
            if submited_form.is_valid():
                rendered_form = self.get_form(next_form_class)
                return HttpResponse(rendered_form)
            else:
                submited_form.errors.update(
                    {'errors_marker_key': 'errors_marker_value'})
                json_data = json.dumps(submited_form.errors)
                return HttpResponse(
                    json_data, {'content_type': 'application/json'})
        return render(request, self.template_name)


def next_rent_form_class(next_step):
    form_classes = [CarRentForm1, CarRentForm2, CarRentForm3, CarRentForm4]
    form_class = form_classes[next_step]
    return form_class


def user_profile(request):
    base_user = User.objects.get(username=request.user.username)
    user = CommonUser.objects.get(user=base_user)
    return render(request, 'user_profile.html', {'common_user': user})
