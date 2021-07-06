from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages
# a flash msg is a way to send a one-time msg to the template.
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

 # Django's login_required function is used to secure views in your web applications by forcing the client to authenticate with a valid logged-in User.
# we're gonna put inn something called Login Decorators above all of our views that we want restricted.
# Create your views here.
from .models import *
from .forms import OrderForm, CreateUserForm, CustomerForm
from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users, admin_only

#
@unauthenticated_user
def registerPage(request):

    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()    #when we save this form its gonna create that user
            username = form.cleaned_data.get('username')  # this allows us to get that username without getting any othr form attributes and at this point we have our flash msg that gets sent , we redirect to the login page.

            messages.success(request, 'Account was created for ' + username)

            return redirect('login')


    context = {'form':form}
    return render(request, 'accounts/register.html', context)

@unauthenticated_user
def loginPage(request):
# #  # our login form sends our username and password ans postdata
# #
    if request.method == 'POST': # checking if the method is post or not.
        username = request.POST.get('username')
        password =request.POST.get('password')

        user = authenticate(request, username=username, password=password)

 #once we authenticate it we first wanna check if tht user is actually there before we redirect him .

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'accounts/login.html', context)

def logoutUser(request):
    logout(request) # it handles logging the user out.
    return redirect('login')

@login_required(login_url= 'login')  # if the user is not logges in go ahead and set the login url and sent them bck to this page so w want to send them back to login page.
@admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'orders':orders, 'customers':customers,
    'total_orders':total_orders,'delivered':delivered,
    'pending':pending }

    return render(request, 'accounts/dashboard.html', context)

@login_required(login_url= 'login')
@allowed_users(allowed_roles =['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all() # thiis allows us to grab all of this customers orders  # orders are relevant to the customers not the users.

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    print('ORDERS:',orders)

    context = {'orders':orders, 'total_orders':total_orders,'delivered':delivered,
    'pending':pending }
    return render(request, 'accounts/user.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
	customer = request.user.customer
	form = CustomerForm(instance=customer)

	if request.method == 'POST':
		form = CustomerForm(request.POST, request.FILES,instance=customer)
		if form.is_valid():
			form.save()


	context = {'form':form}
	return render(request, 'accounts/account_settings.html', context)




@login_required(login_url= 'login')
@allowed_users(allowed_roles =['admin'])
def products(request):
    products = Product.objects.all()

    return render(request, 'accounts/products.html', {'products':products})


@login_required(login_url= 'login')
@allowed_users(allowed_roles =['admin'])
def customer(request, pk_test):

    customer = Customer.objects.get(id=pk_test)

    orders = customer.order_set.all()
    order_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders) # we're actually gonna send request data to this view and its gonna take in a query set whic is orders, we're first going to query  all the orders ,we gonna throw them into this filter  and then based on what tht request data is we're gonna filter this data down
    # we'll rebuild that orders variable and we're gonna keep the same name.
    orders = myFilter.qs # first orders gets rendered thrown into the filter if we have any parameters it cleans it , it filters it down and then we remake that variable with the filter down data.

    context = {'customer':customer, 'orders':orders, 'order_count':order_count,'myFilter': myFilter}
    return render(request, 'accounts/customer.html',context)

@login_required(login_url= 'login')
@allowed_users(allowed_roles =['admin'])
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product','status'), extra=10) # initial formset factory   # customer is parent model and order is child model.its gonna have references from order to customer.
    # we're gonna have multiple orders so we need to tell it which fields we want to allow for the child objects , here whichare products and status.
    customer = Customer.objects.get(id=pk) # parent model customer
    formset = OrderFormSet(queryset= Order.objects.none() ,instance = customer) # in order too hide the first filled value we need to throw in something into this intial instance     # we're passing the instance of the customer, now that we threw in the parents we can acctually reference that model
    #form = OrderForm(initial={'customer':customer}) # here customer is dict   # we'll set an instance, we've already selected a customer what we're gonna do is pass in an instance of the customer and this is why we query the customer here.
    if request.method == 'POST':
        #print('Printing POST:', request.POST)
        form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST,instance = customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'form':formset}
    return render(request, 'accounts/order_form.html', context)

@login_required(login_url= 'login')
@allowed_users(allowed_roles =['admin'])
def updateOrder(request, pk):

    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form':form}
    return render(request, 'accounts/order_form.html', context)

@login_required(login_url= 'login')
@allowed_users(allowed_roles =['admin'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk) # for prefilled value
    if request.method == "POST":
        order.delete()
        return redirect('/') # it'll redirect us to the main page tht is dashboard

    context = {'item':order}
    return render(request, 'accounts/delete.html', context)










#when to use instance and when to use initial.?
#Ans = there's quite a difference. "Initial" is used to set the initial
# values and is quite appropriate when a new model instance is going to
# be created. The "instance" is used when you want the ModelForm to be
# used to update an existing instance of a model. Since Django does not
# currently incorporate mind-reading technology, if the two parameters
# were merged into one, the framework wouldn't know whether it's meant to
# be updating an existing instance or creating a new one."
