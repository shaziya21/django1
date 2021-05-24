from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from .models import *

def home(request):
    orders = order.objects.all()
    customers = customer.objects.all()
    context = {'orders' : orders, 'customers': customers}

    return render(request,'accounts/dashboard.html')

def products(request):
    products = product.objects.all()  # this gonna go ahead and query the database for all products & we can pass this intothe template by throwing in a dictionary as one parameter to this render fn.
    return render(request,'accounts/products.html',{'products' : products}) # for key we need to pass in the key as the valueswhatever we want and this can be called just a list or whatever we want it but whatever we say here


def customer(request):
    return render(request,'accounts/customer.html')
