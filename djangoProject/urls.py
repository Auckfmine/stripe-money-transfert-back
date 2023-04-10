from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("stripe/", include('stripe_demo.urls'))

]
