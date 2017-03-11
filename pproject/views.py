import braintree
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings


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
        return HttpResponse("Failed to generate Braintree client token", status=500)

    return render(request, template_name, {"bt_client_token": client_token})
