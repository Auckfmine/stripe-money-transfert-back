
from .views import StripeAPI
from django.urls import path

urlpatterns = [
    path("transfert", StripeAPI.as_view({'post': 'transfer_user_a_user_b'})),
    path("balance/<str:account_id>", StripeAPI.as_view({'get': 'retrieve_account_balance'})),
]
