import json

from django.shortcuts import render, redirect, render_to_response
from django.views.generic.edit import FormView
from django.views.generic.edit import CreateView
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.contrib.auth.models import User

from pproject.models import CommonUser, Car
from pproject.forms import CarRentForm1, CarRentForm2, CarRentForm3, \
    CarRentForm4, CarRentForm5, RegistrationMultiForm, LoginForm, \
    QuickSearchForm


def main(request):
    form = LoginForm
    quick_search_form = QuickSearchForm
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            new_user = authenticate(username=form.cleaned_data['email'],
                                    password=form.cleaned_data['password'])
            login(request, new_user)
    if request.POST and request.POST['rental_perion_begin']:
        quick_search_form = QuickSearchForm(request.POST)
        if form.is_valid():
            return redirect(reverse('search'),
                            {'quick_search_form': quick_search_form})
    if (request.user.is_authenticated() and
            not request.user.is_superuser and
            not request.user.is_staff):
        base_user = User.objects.get(username=request.user.username)
        user = CommonUser.objects.get(user=base_user)
    elif request.user.is_superuser or request.user.is_staff:
        user = User.objects.get(username=request.user.username)
    else:
        user = ''
    return render(request, 'main.html', {
        'form': form,
        'common_user': user,
        'quick_search_form': quick_search_form})


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
    form and get it in js.
    """

    form_class = CarRentForm1
    form_classes = [
        CarRentForm1, CarRentForm2,
        CarRentForm3, CarRentForm4,
        CarRentForm5]
    form_step_template = [
        'rent_car_form_steps/step0.html',
        'rent_car_form_steps/step1.html',
        'rent_car_form_steps/step2.html',
        'rent_car_form_steps/step3.html',
        'rent_car_form_steps/step4.html']
    template_name = 'set_car_rent.html'
    car_data_dict = {}
    car_created = False

    def get(self, request, *args, **kwargs):
        form0 = self.form_class()
        if request.is_ajax():
            return render_to_response(
                self.form_step_template[0], {'form0': form0})
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
            if next_step < len(self.form_classes):
                next_form_class = next_rent_form_class(next_step)
            val_form = self.form_classes[next_step - 1]
            submited_form = val_form(request.POST)
            if submited_form.is_valid():
                self.car_data_dict.update(submited_form.cleaned_data)
                if val_form is self.form_classes[-1] and not self.car_created:
                    new_car = Car.objects.create(**self.car_data_dict)
                    self.car_created = True
                    if (self.request.user.is_authenticated() and
                            not self.request.user.is_superuser and
                            not self.request.user.is_staff):
                        base_user = User.objects.get(
                            username=self.request.user.username)
                        user = CommonUser.objects.get(user=base_user)
                        new_car.owner = user
                        new_car.save()
                    # redirect calls self.get() which render redirect page
                    # in current view so we'd redirect via js
                    return HttpResponse('OK')

                if next_step < len(self.form_classes):
                    rendered_form = self.get_form(next_form_class)
                    return render_to_response(
                        self.form_step_template[next_step],
                        {'form': rendered_form})
            else:
                submited_form.errors.update(
                    {'errors_marker_key': 'errors_marker_value'})
                json_data = json.dumps(submited_form.errors)
                return HttpResponse(
                    json_data, {'content_type': 'application/json'})
        return render(request, self.template_name)


def next_rent_form_class(next_step):
    form_classes = [CarRentForm1, CarRentForm2,
                    CarRentForm3, CarRentForm4,
                    CarRentForm5]
    form_class = form_classes[next_step]
    return form_class


def user_profile(request):
    base_user = User.objects.get(username=request.user.username)
    user = CommonUser.objects.get(user=base_user)
    return render(request, 'user_profile.html', {'common_user': user})
