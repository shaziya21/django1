from django.contrib import admin

# Register your models here.
from .models import * # importing model
admin.site.register(customer) # registering the customer model
admin.site.register(product)
admin.site.register(tag)
admin.site.register(order)
