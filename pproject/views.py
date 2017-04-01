import json

from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views import View

from pproject.forms import CarRentForm1, CarRentForm2, CarRentForm3


def main(request):
    return render(request, "main.html")


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
