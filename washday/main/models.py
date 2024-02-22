from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    phone = PhoneNumberField()
    address = models.CharField(max_length=256)


class LaundryItem(models.Model):
    CATEGORY_CHOICES = [
        ('Men', 'Men'),
        ('Women', 'Women'),
        ('Household Linen', 'Household Linen'),
    ]
    itemID = models.CharField(max_length=10, blank=False, primary_key=True)
    name = models.CharField(max_length=100)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)


class Order(models.Model):
    PRIORITY_CHOICES = [
        ('Normal', 'Normal'),
        ('Urgent', 'Urgent'),
        ('Very Urgent', 'Very Urgent'),
    ]

    PAYMENT_CHOICES = [
        ('Visa/MasterCard', 'Visa/MasterCard'),
        ('Payment on Delivery', 'Payment on Delivery'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Complete', 'Complete'),
    ]

    orderID = models.CharField(max_length=10, blank=False, primary_key=True)
    pickup_date = models.DateField()
    pickup_time = models.TimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    priority = models.CharField(max_length=11, choices=PRIORITY_CHOICES)
    payment_method = models.CharField(max_length=19, choices=PAYMENT_CHOICES)
    address = models.CharField(max_length=64, blank=False)
    instruction = models.CharField(max_length=64, blank=True)
    total_items = models.IntegerField(blank=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    order_status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    payment_status = models.CharField(max_length=20, choices=STATUS_CHOICES)


class BagDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='bag_details')
    item = models.ForeignKey(LaundryItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
