import json

from rest_framework.views import APIView
from rest_framework.response import Response

from config import settings
from .serializer import *
from rest_framework import generics, permissions, status, views
import stripe
from decimal import Decimal
from django.conf import settings


class CreatePaymentIntetn(APIView):
    def post(self, request):
        if request.method == 'POST':
            stripe.api_key = settings.STRIPE_SECRET
            user = request.data.get('user')
            cart = request.data.get('cart')

            tax_list = [0.115 if user['state'] == 'PR' else 0]
            items = [c["name"] for c in cart]
            qty = [c["qty"] for c in cart]

            subtotal = []
            for i in cart:
                item_id = i.get('itemId')
                qty = i.get('qty')
                p = Product.objects.get(pk=item_id)

                # Validate product inventory
                if p.inventory == 0:
                    return Response(
                        data={
                            'message': 'One of your products is sold out'},
                        status=status.HTTP_409_CONFLICT)

                subtotal.append(p.price * qty)

            # total calculations
            tax = round(sum(subtotal) * Decimal(tax_list[0]), 2)
            total = round(Decimal(sum(subtotal) + tax), 2)
            stripe_total = int(total * 100)

            intent = stripe.PaymentIntent.create(
                amount=stripe_total,
                currency="usd",
                automatic_payment_methods={"enabled": True},
            )
            return Response(data={
                'tax': tax,
                'client_secret': intent.client_secret
            }, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    # def post(self, request):
    #     stripe.api_key= settings.STRIPE_SECRET_KEY
    #     payment = stripe.PaymentIntent.create(
    #         amount = 1000,
    #         currency = 'usd',
    #         automatic_payment_methods = {'enabled':True}
    #     )
    #     return Response(payment.client_secret)

class WebhookReceived(APIView):
    def post(self, request):

        webhook_secret = settings.STRIPE_WEBHOOK_SECRET
        request_data = json.loads(request.data)

        if webhook_secret:
            signature = request.headers.get('stripe_signature')
            try:
                 event = stripe.Webhook.construct_event(
                     payload=request.data, sig_header=signature, secret=webhook_secret),
                 data = event['data']
            except Exception as e:
                return e

            event_type = event['type']
        else:
            data = request_data['data']
            event_type = request_data['type']
        data_object = data['object']

        if event_type == 'payment.succeeded':
            print("Payment received")
        return Response({'status':'success'})