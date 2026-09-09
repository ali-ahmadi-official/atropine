from django.urls import path
from .views import (
    start_payment,
    verify_payment,
    verify_kiani_payment,
    check_pending_payments
)

urlpatterns = [
    path(
        "start/<int:package_id>/<str:provider>/",
        start_payment,
        name="payment_start"
    ),

    path(
        "verify/",
        verify_payment,
        name="payment_verify"
    ),

    path(
        "verify/kiani/",
        verify_kiani_payment,
        name="verify_kiani_payment",
    ),

    path(
        "check-pending/",
        check_pending_payments,
        name="check_pending_payments"
    ),
]