

import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from packs.models import UnlockedPack, Pack
from django.contrib.auth.models import User


@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except Exception:
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

        user_id = session["metadata"]["user_id"]
        pack_id = session["metadata"]["pack_id"]

        user = User.objects.get(id=user_id)
        pack = Pack.objects.get(id=pack_id)

        UnlockedPack.objects.get_or_create(user=user, pack=pack)

    return HttpResponse(status=200)
