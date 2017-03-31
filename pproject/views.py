import braintree
import json
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.conf import settings
from django.views import View

from pproject.forms import CarRentForm1, CarRentForm2, \
    CarRentForm3, CarRentForm4


braintree.Configuration.configure(braintree.Environment.Sandbox,
                                  merchant_id=settings.BRAINTREE_MERCHANT_ID,
                                  public_key=settings.BRAINTREE_PUBLIC_KEY,
                                  private_key=settings.BRAINTREE_PRIVATE_KEY,)


def start_payment_view(request, template_name="start_payment.html"):
    """
    Generate client token and pass it in the view context.
    """
    try:
        client_token = braintree.ClientToken.generate()
    except ValueError as e:
        return HttpResponse("Failed to generate Braintree client token",
                            status=500)

    return render(request, template_name, {"bt_client_token": client_token})


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
