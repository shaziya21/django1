from django.contrib import admin

# Register your models here.
from .models import * # importing model
admin.site.register(Customer) # registering the customer model
admin.site.register(Product)
admin.site.register(Tag)
admin.site.register(Order)
