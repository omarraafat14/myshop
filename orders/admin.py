from django.contrib import admin
from django.utils.safestring import mark_safe
from django.urls import reverse
from orders.admin_actions import export_to_csv
from .models import Order, OrderItem


# Register your models here.
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ["product"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "first_name",
        "last_name",
        "email",
        "address",
        "postal_code",
        "city",
        "paid",
        "order_payment",
        "created",
        "updated",
        "order_detail",
        "order_pdf",
    ]
    list_filter = ["paid", "created", "updated"]
    inlines = [OrderItemInline]
    actions = [export_to_csv]

    def order_payment(self, obj):
        url = obj.get_stripe_url()
        if obj.stripe_id:
            html = f'<a href="{url}" target="_blank">{obj.stripe_id}</a>'
            return mark_safe(html)
        return ""

    order_payment.short_description = "Stripe payment"

    def order_detail(self, obj):
        url = reverse("orders:admin_order_detail", args=[obj.id])
        return mark_safe(f'<a href="{url}">View</a>')

    def order_pdf(self, obj):
        url = reverse("orders:admin_order_pdf", args=[obj.id])
        return mark_safe(f'<a href="{url}">PDF</a>')

    order_pdf.short_description = "Invoice"
