import datetime

from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import GenericViewSet
import stripe
from rest_framework.response import Response
from rest_framework import status
from stripe.error import StripeError
from django.conf import settings

class StripeAPI(GenericViewSet):
    def __init__(self):
        stripe.api_key = settings.STRIPE_SECRET_KEY

    def retrieve_account_balance(self, request, account_id):
        try:
            balance = stripe.Balance.retrieve(
                stripe_account=account_id
            )
            return Response(data={"success": True, "data": balance})
        except stripe.error.StripeError as e:
            return Response(data={"success": False, "error": str(e)}, status=400)
        except Exception:
            return Response(data={"success": False, "error": "something wrong"}, status=400)

    def transfer_user_a_user_b(self, request):
        sender_id = request.data['sender_id']
        recipient_id = request.data['recipient_id']
        amount = request.data['amount']
        currency = request.data['currency']
        sender_card = request.data['sender_card_token'],
        description = request.data['description']
        try:

            # Create a charge on the sender's customer
            charge = stripe.Charge.create(
                            amount=int(amount)*100,
                            currency=currency,
                            source=sender_id,
                            description=description,
                            on_behalf_of=sender_id,)

            # Transfer the funds to the recipient's connected account
            transfer = stripe.Transfer.create(
                amount=int(amount)*100,
                currency=currency,
                destination=recipient_id,
                source_transaction=charge.id,
            )
            return Response(data={"success": True, "data": transfer})
        except stripe.error.StripeError as e:
            print("Error:", e)
            return Response(data={"success": False, "error": str(e)}, status=400)
        except Exception as e :
            print(str(e))
            return Response(data={"success": False, "error": "something wrong"}, status=400)

