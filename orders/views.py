from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.conf import settings
import weasyprint
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created


def order_create(request):
    """
    Create an order from the cart items.

    This view handles the creation of an order from the items present in the cart. If the request method is POST,
    it attempts to create an order using the submitted form data. If the form is valid, it saves the order,
    creates order items for each item in the cart, clears the cart, launches a task to send an email notification,
    sets the order ID in the session for further processing (like payment), and then redirects to the payment process.
    If the request method is not POST, it simply displays the order form to the user.

    Parameters:
    - request (HttpRequest): The incoming request object containing the cart and possibly the form data for creating an order.

    Returns:
    - HttpResponse: A response object that either redirects to the payment process upon successful order creation
      or renders the order creation form page with the current cart contents.
    """
    cart = Cart(request)
    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    price=item["price"],
                    quantity=item["quantity"],
                )
            cart.clear()
            # lunch a celery task to send an e-mail
            order_created.delay(order.id)
            # set the order in the session
            request.session["order_id"] = order.id
            # redirect for payment
            return redirect(reverse("payment:process"))
            return render(request, "orders/order/created.html", {"order": order})
    else:
        form = OrderCreateForm()
    return render(request, "orders/order/create.html", {"cart": cart, "form": form})


@staff_member_required
def admin_order_detail(request, order_id):
    """
    Display the detail of an order in the admin site.

    This view is restricted to staff members only. It retrieves an order by its ID and displays its details
    on a dedicated page. If the order does not exist, it raises a 404 error.

    Parameters:
    - request (HttpRequest): The incoming request object.
    - order_id (int): The unique identifier of the order to be retrieved.

    Returns:
    - HttpResponse: A response object that renders the 'admin/orders/order/detail.html' template,
      populated with the order details.
    """
    order = get_object_or_404(Order, id=order_id)
    return render(request, "admin/orders/order/detail.html", {"order": order})


@staff_member_required
def admin_order_pdf(request, order_id):
    """
    Generate a PDF version of the order details for the admin.

    Parameters:
    request (HttpRequest): The incoming request object.
    order_id (int): The unique identifier of the order.

    Returns:
    HttpResponse: A response object with the generated PDF file.

    This function retrieves the order details from the database using the provided order_id.
    It then renders the order details into an HTML template.
    The HTML content is converted into a PDF using the WeasyPrint library.
    The generated PDF is attached to a response object with the appropriate content type and filename.
    Finally, the response object is returned to the client.
    """
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string("orders/order/pdf.html", {"order": order})
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f"filename=order_{order.id}.pdf"
    weasyprint.HTML(string=html).write_pdf(
        response, stylesheets=[weasyprint.CSS(settings.STATIC_ROOT / "css/pdf.css")]
    )
    return response
