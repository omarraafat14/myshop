from io import BytesIO
from celery import shared_task
import weasyprint
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from orders.models import Order


@shared_task
def payment_completed(order_id):
    """
    Task to send an invoice email to the customer upon payment completion.

    This function retrieves an order using the provided order_id, generates an invoice in PDF format,
    and sends it to the customer's email address.

    Parameters:
    - order_id (int): The ID of the order for which the payment has been completed.

    The function does not return any value but sends an email with the attached invoice PDF.
    """
    order = Order.objects.get(id=order_id)
    # Create invoice e-mail
    subject = f"My Shop - Inovice for order {order.id}"
    message = f"Dear {order.first_name},\n\nThank you for your order. Your invoice is attached."
    email = EmailMessage(
        subject=subject,
        message=message,
        from_email="admin@myshop.com",
        to=[order.email],
    )
    # Generate PDf
    html = render_to_string("orders/order/pdf.html", {"order": order})
    # Create a BytesIO object to store the PDF data
    out = BytesIO()
    weasyprint.HTML(string=html).write_pdf(
        out, stylesheets=[weasyprint.CSS(settings.STATIC_ROOT / "css/pdf.css")]
    )
    # Attach PDF to e-mail
    email.attach(f"order_{order.id}.pdf", out.getvalue(), "application/pdf")
    # Send e-mail
    email.send()
