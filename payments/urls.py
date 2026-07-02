from django.urls import path
from .views import (
    start_payment,
    verify_payment
)

urlpatterns = [
    path(
        "start/<int:package_id>/",
        start_payment,
        name="payment_start"
    ),

    path(
        "verify/",
        verify_payment,
        name="payment_verify"
    ),
]