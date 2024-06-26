from django.db import models
from shop.models import Product
from django.core.validators import MinValueValidator, MaxValueValidator
from coupons.models import Coupon
from .model_mixins import OrderMixin


class Order(OrderMixin, models.Model):
    # main info
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    # dates
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # payment info
    paid = models.BooleanField(default=False)
    stripe_id = models.CharField(max_length=250, blank=True)
    # coupons
    coupon = models.ForeignKey(
        Coupon,
        related_name="orders",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    discount = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )

    class Meta:
        ordering = ["-created"]
        indexes = [
            models.Index(fields=["-created"]),
        ]

    def __str__(self):
        return f"Order {self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name="items",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product, related_name="order_items", on_delete=models.CASCADE
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
