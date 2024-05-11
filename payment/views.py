from decimal import Decimal
from decouple import config
import stripe
from django.shortcuts import render, redirect, reverse, get_object_or_404
from orders.models import Order


# create the Stripe instance
stripe.api_key = config("STRIPE_SECRET_KEY")
stripe.api_version = config("STRIPE_API_VERSION")


def payment_process(request):
    order_id = request.session.get("order_id", None)
    order = get_object_or_404(Order, id=order_id)
    if request.method == "POST":
        success_url = request.build_absolute_uri(reverse("payment:completed"))
        cancel_url = request.build_absolute_uri(reverse("payment:canceled"))
        # Stripe checkout session data
        session_data = {
            "mode": "payment",  # for a one-time payment
            "client_reference_id": order.id,  # to reconcile the Stripe checkout session with our order.
            "success_url": success_url,  # redirect to this URL after the payment is successful.
            "cancel_url": cancel_url,  # redirect to this URL after the payment is canceled.
            "line_items": [],  # add the order items to the checkout session.
        }
        # add order items to the Stripe checkout session
        for item in order.items.all():
            session_data["line_items"].append(
                {
                    "price_data": {
                        "unit_amount": int(item.price * Decimal("100")),
                        "currency": "usd",
                        "product_data": {
                            "name": item.product.name,
                        },
                    },
                    "quantity": item.quantity,
                }
            )
        # Stripe coupon
        if order.coupon:
            stripe_coupon = stripe.Coupon.create(
                name=order.coupon.code,
                percent_off=order.coupon.discount,
                duration="once",
            )
            session_data["discounts"] = [
                {
                    'coupon': stripe_coupon.id,
                }
            ]
        # create Stripe checkout session
        session = stripe.checkout.Session.create(**session_data)
        # redirect to Stripe payment form
        # The status code 303 is recommended to redirect web applications to a new URI after an HTTP POST has been performed
        return redirect(session.url, code=303)
    else:
        return render(request, "payment/process.html", locals())


def payment_completed(request):
    return render(request, "payment/completed.html")


def payment_canceled(request):
    return render(request, "payment/canceled.html")
