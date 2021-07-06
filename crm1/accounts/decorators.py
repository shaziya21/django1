from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
# this autenticated_user is a view based function & view_func is loginpage in this case.
# now all we have is this decorator(unauthenticated_user) that gets called when the login page view is called then the condition is checked

    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func

def allowed_users(allowed_roles=[]): # we're creating a three layers functions
    def decorator(view_func):
        def wrapper_func(request,*args,**kwargs):

            group = None
            if request.user.groups.exists():  # checking if user is part of group or not
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to view this page')
        return wrapper_func
    return decorator

#set some functionality to make sure that a page is restrictive,so we're setting a variable called group


def admin_only(view_func):
    def wrapper_function(request,*args,**kwargs):
            group = None
            if request.user.groups.exists():  # checking if user is part of group or not
                group = request.user.groups.all()[0].name

            if group == 'customer':
                return redirect('user-page')

            if group == 'admin':
                return view_func(request,*args,**kwargs)

    return wrapper_function
