from django.contrib import admin  # noqa: F401

from .models import BagDetail, LaundryItem, Order, User

# Register your models here.
admin.site.register(User)
admin.site.register(LaundryItem)
admin.site.register(Order)
admin.site.register(BagDetail)
