import json
import urllib
import datetime
import unicodedata
import os
from django.shortcuts import render, redirect, render_to_response
from django.views.generic.edit import FormView
from django.views.generic.edit import CreateView
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.contrib.auth.models import User

from django.core.files import File
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings

from pproject.models import CommonUser, Car, CommentCarOwner, CommentCar
from pproject.forms import CarRentForm1, CarRentForm2, CarRentForm3, \
    CarRentForm4, CarRentForm5, RegistrationMultiForm, LoginForm, \
    QuickSearchForm, SearchForm, EditMultiForm, CommentCarOwnerForm, \
    CommentCarForm


def header_search(request):
    return JsonResponse({
        'success_url':
        reverse('search') + '?' +
            'quicksearch=True&' +
            'headersearch=True&' +
            'city=' + request.POST['header_search']})


def main(request):
    form = LoginForm
    quick_search_form = QuickSearchForm
    popular_ads = Car.objects.order_by('-times_rented')[:10]
    sorted_ads_by_popularity = Car.objects.order_by('-city')
    re_sorted_ads_by_popularity = list(sorted_ads_by_popularity)
    i = 0
    while i < len(re_sorted_ads_by_popularity) - 1:
        if (re_sorted_ads_by_popularity[i].city ==
                re_sorted_ads_by_popularity[i + 1].city):
            del re_sorted_ads_by_popularity[i + 1]
        else:
            i = 0

    if 'rental_perion_begin' in request.POST:
        quick_search_form = QuickSearchForm(request.POST)
        if quick_search_form.is_valid():
            for item in quick_search_form.cleaned_data:
                if not isinstance(
                        quick_search_form.cleaned_data[item], datetime.date):
                    quick_search_form.cleaned_data[item] = \
                        quick_search_form.cleaned_data[item].encode('utf8')
            return redirect(
                reverse('search') + '?' + 'quicksearch=True&' +
                urllib.urlencode(quick_search_form.cleaned_data))
    if request.POST and not request.user.is_authenticated():
        form = LoginForm(request.POST)
        if form.is_valid():
            new_user = authenticate(username=form.cleaned_data['email'],
                                    password=form.cleaned_data['password'])
            login(request, new_user)
    if (request.user.is_authenticated() and
            not request.user.is_superuser and
            not request.user.is_staff):
        base_user = User.objects.get(username=request.user.username)
        user = CommonUser.objects.get_or_create(user=base_user)[0]
    elif request.user.is_superuser or request.user.is_staff:
        user = User.objects.get(username=request.user.username)
    else:
        user = ''
    return render(request, 'main.html', {
        'form': form,
        'common_user': user,
        'quick_search_form': quick_search_form,
        'popular_ads': popular_ads,
        'sorted_ads_by_popularity': re_sorted_ads_by_popularity[:10]})


def search(request):
    adv_search_form = SearchForm
    searched_cars = Car.objects.none()
    price_searched_cars = Car.objects.none()
    year_searched_cars = Car.objects.none()
    mileage_searched_cars = Car.objects.none()
    if request.POST and not request.user.is_authenticated():
        form = LoginForm(request.POST)
        if form.is_valid():
            new_user = authenticate(username=form.cleaned_data['email'],
                                    password=form.cleaned_data['password'])
            login(request, new_user)
    if (request.user.is_authenticated() and
            not request.user.is_superuser and
            not request.user.is_staff):
        base_user = User.objects.get(username=request.user.username)
        user = CommonUser.objects.get_or_create(user=base_user)[0]
    elif request.user.is_superuser or request.user.is_staff:
        user = User.objects.get(username=request.user.username)
    else:
        user = ''
    if 'quicksearch' in request.GET:
        qsearch_dict = dict(request.GET.iterlists())
        qsearch_dict.pop('quicksearch')
        if 'headersearch' not in request.GET:
            date1 = datetime.datetime.\
                strptime(
                    qsearch_dict['rental_perion_begin'][0], '%Y-%m-%d').date()
            date2 = datetime.datetime.\
                strptime(
                    qsearch_dict['rental_perion_end'][0], '%Y-%m-%d').date()
            day_count = (date2 - date1).days
            for single_begin_date in (
                    date1 + datetime.timedelta(n) for n in range(day_count)):
                searched_cars = searched_cars | Car.objects.filter(
                    city=qsearch_dict['city'][0],
                    rental_perion_begin=single_begin_date)
        else:
            searched_cars = searched_cars | Car.objects.filter(
                city=qsearch_dict['city'][0])
        if len(searched_cars) < 2:
            idx = 0
        else:
            idx = len(searched_cars) - 2
        if request.is_ajax():
            return render_to_response(
                'quick_searched_cars.html',
                {'searched_cars': searched_cars[:idx]})
        return render(
            request,
            'search.html',
            {'searched_cars': searched_cars[
                idx:len(searched_cars)],
             'form': adv_search_form,
             'search_params': qsearch_dict,
             'common_user': user})
    elif request.POST and request.is_ajax():
        qsearch_dict = dict(request.POST.iterlists())
        pre_data = {
            'car_type': qsearch_dict['car_type'][0],
            'fuel': qsearch_dict['fuel'][0],
            'transmission': qsearch_dict['transmission'][0],
            'condition': qsearch_dict['condition'][0],
            'model': qsearch_dict['model'][0]
        }
        for item in pre_data.keys():
            if not unicodedata.normalize('NFKD', pre_data[item]).encode(
                    'ascii', 'ignore'):
                del pre_data[item]

        searched_cars = searched_cars | Car.objects.filter(**pre_data)

        if qsearch_dict['price1'][0] and qsearch_dict['price2'][0]:
            prices1 = set(range(int(qsearch_dict['price1'][0])))
            prices2 = set(range(int(qsearch_dict['price2'][0]) + 1))
            price_list = []
            for oprice in list(prices2 - prices1):
                if oprice % 100 == 0:
                    price_list.append(oprice)

            for some_price in price_list:
                p_searched_cars = searched_cars.filter(
                    price=some_price)
                if p_searched_cars:
                    price_searched_cars = price_searched_cars | p_searched_cars
            searched_cars = price_searched_cars

        if qsearch_dict['myear1'][0] and qsearch_dict['myear2'][0]:
            myears1 = set(range(int(qsearch_dict['myear1'][0])))
            myears2 = set(range(int(qsearch_dict['myear2'][0]) + 1))
            for year in list(myears2 - myears1):
                if price_searched_cars:
                    y_searched_cars = price_searched_cars.filter(
                        issue_date=year)
                else:
                    y_searched_cars = searched_cars.filter(
                        issue_date=year)
                if y_searched_cars:
                    year_searched_cars = year_searched_cars | y_searched_cars
            searched_cars = year_searched_cars
        if qsearch_dict['mileage1'][0] and qsearch_dict['mileage2'][0]:
            mieages1 = set(range(int(qsearch_dict['mileage1'][0])))
            mieages2 = set(range(int(qsearch_dict['mileage2'][0]) + 1))
            for some_mileage in list(mieages2 - mieages1):
                if year_searched_cars:
                    m_searched_cars = year_searched_cars.filter(
                        mileage=some_mileage)
                elif price_searched_cars and not year_searched_cars:
                    m_searched_cars = price_searched_cars.filter(
                        mileage=some_mileage)
                else:
                    m_searched_cars = searched_cars.filter(
                        mileage=some_mileage)
                if m_searched_cars:
                    mileage_searched_cars = mileage_searched_cars | m_searched_cars
            searched_cars = mileage_searched_cars

        return render_to_response(
            'quick_searched_cars.html',
            {'searched_cars': searched_cars})

    return render(request, 'search.html', {
        'form': adv_search_form, 'common_user': user})


def book_a_car(request, car_id):
    comment_form = CommentCarForm
    form = LoginForm
    comments = CommentCar.objects.all()
    car_comments = comments_paginator(comments, request)
    if request.POST and not request.user.is_authenticated():
        form = LoginForm(request.POST)
        if form.is_valid():
            new_user = authenticate(username=form.cleaned_data['email'],
                                    password=form.cleaned_data['password'])
            login(request, new_user)
    if (request.user.is_authenticated() and
            not request.user.is_superuser and
            not request.user.is_staff):
        base_user = User.objects.get(username=request.user.username)
        user = CommonUser.objects.get_or_create(user=base_user)[0]
    elif request.user.is_superuser or request.user.is_staff:
        user = User.objects.get(username=request.user.username)
    else:
        user = ''
    car = Car.objects.get(id=car_id)

    if 'complete_booking' in request.GET:
        return redirect(
            reverse('complete_booking') + '?' + 'car_id=' + car_id)

    post_comment_form = CommentCarForm(request.POST)
    if request.user.is_authenticated():
        if post_comment_form.is_valid():
            CommentCar.objects.create(
                comment_author=user,
                commented_car=Car.objects.get(id=car_id),
                **post_comment_form.cleaned_data)
    else:
        if post_comment_form.is_valid():
            CommentCar.objects.create(
                commented_car=Car.objects.get(id=car_id),
                **post_comment_form.cleaned_data)

    return render(request, 'book_a_car.html', {
        'common_user': user,
        'car': car,
        'comment_form': comment_form,
        'form': form,
        'comments': car_comments,
        'count_comments': comments.count()})


def complete_booking(request):
    return render(request, 'complete_booking.html')


def help(request):
    form = LoginForm
    if request.POST and not request.user.is_authenticated():
        form = LoginForm(request.POST)
        if form.is_valid():
            new_user = authenticate(username=form.cleaned_data['email'],
                                    password=form.cleaned_data['password'])
            login(request, new_user)
    if (request.user.is_authenticated() and
            not request.user.is_superuser and
            not request.user.is_staff):
        base_user = User.objects.get(username=request.user.username)
        user = CommonUser.objects.get_or_create(user=base_user)[0]
    elif request.user.is_superuser or request.user.is_staff:
        user = User.objects.get(username=request.user.username)
    else:
        user = ''
    return render(request, 'how-this-work.html', {
        'common_user': user,
        'form': form})


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


tmp_file = ''
path = ''


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
        base_user = User.objects.get(username=request.user.username)
        user = CommonUser.objects.get(user=base_user)
        if request.is_ajax():
            return render_to_response(
                self.form_step_template[0], {'form0': form0})
        return render(request, self.template_name, {'common_user': user})

    def post(self, request, *args, **kwargs):
        """
        Form post.

        Post current form and prepare the next one for loading via js.
        As it could return either next form of current form errors,
        form errors updates by special marker to differentiate form
        from form errors

        """
        global tmp_file, path
        if request.is_ajax():
            next_step = int(request.POST['next_step'])
            if next_step < len(self.form_classes):
                next_form_class = next_rent_form_class(next_step)
            val_form = self.form_classes[next_step - 1]
            submited_form = val_form(request.POST, request.FILES)
            if 'photo' in request.FILES:
                path = default_storage.save(
                    request.FILES['photo'].name,
                    ContentFile(request.FILES['photo'].read()))
                tmp_file = os.path.join(settings.MEDIA_ROOT, path)

            if submited_form.is_valid():
                self.car_data_dict.update(submited_form.cleaned_data)
                if val_form is self.form_classes[-1] and not self.car_created:
                    if tmp_file:
                        with open(tmp_file, 'r+') as f:
                            photo = File(f)
                            self.car_data_dict.pop('photo')

                            new_car = Car.objects.create(**self.car_data_dict)
                            new_car.photo.save(path, photo, save=True)
                    else:
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


def user_profile(request, user_id):
    form = EditMultiForm
    comment_form = CommentCarOwnerForm
    base_user = User.objects.get(username=request.user.username)
    user = CommonUser.objects.get(user=base_user)
    upd_base_user = User.objects.filter(username=request.user.username)
    upd_user = CommonUser.objects.filter(user=base_user)
    user_cars = Car.objects.filter(owner=user)
    upd_form = form(request.POST)
    new_base_data = {}
    new_data = {}
    if upd_form.is_valid():
        for field1 in upd_form.cleaned_data['base_user']:
            if upd_form.cleaned_data['base_user'][field1]:
                new_base_data.update({
                    field1: upd_form.cleaned_data['base_user'][field1]})
        for field2 in upd_form.cleaned_data['common_user']:
            if upd_form.cleaned_data['common_user'][field2]:
                new_data.update({
                    field2: upd_form.cleaned_data['common_user'][field2]})
        upd_base_user.update(**new_base_data)
        upd_user.update(**new_data)
    post_comment_form = comment_form(request.POST)
    if request.is_ajax() and request.POST:
        is_owner = False
        if user_cars:
            is_owner = True
        if 'like' in request.POST:
            liked_comment = CommentCarOwner.objects.get(
                id=request.POST['like'])
            liked_comment.is_interesting += 1
            liked_comment.save()
        if post_comment_form.is_valid():
            new_comment = CommentCarOwner.objects.create(
                comment_author=user,
                commented_user=CommonUser.objects.get(id=user_id),
                **post_comment_form.cleaned_data)
            return render_to_response(
                'car_owner_comment.html',
                {'new_comment': new_comment,
                 'is_owner': is_owner})

    comments = CommentCarOwner.objects.filter(commented_user=user)
    users_comments = []
    onwers_comments = []
    for comment in comments:
        try:
            cars = Car.objects.get(owner=comment.comment_author)
        except:
            cars = []
        if cars:
            onwers_comments.append(comment)
        else:
            users_comments.append(comment)

    o_comments = comments_paginator(onwers_comments, request)
    u_comments = comments_paginator(users_comments, request)

    return render(request, 'user_profile.html',
                  {'common_user': user,
                   'searched_cars': user_cars,
                   'form': form,
                   'comment_form': comment_form,
                   'onwers_comments': o_comments,
                   'users_comments': u_comments})


def comments_paginator(comments, req):
    paginator = Paginator(comments, 10)
    page = req.GET.get('page')
    try:
        paginated_comments = paginator.page(page)
    except PageNotAnInteger:
        paginated_comments = paginator.page(1)
    except EmptyPage:
        paginated_comments = paginator.page(paginator.num_pages)
    return paginated_comments
