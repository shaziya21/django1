# we're gonna be building a filter, based around a model, so its gonna be a lot like a modelform again  thats gonna build a filter form for us based on  all of these attributes so our model is gonna be order.

import django_filters
from django_filters import DateFilter , CharFilter # adding a date range filter
from .models import *

# build a python class thats going to build a filter for us
class OrderFilter(django_filters.FilterSet):
# creating some custom attributes.
# gte = greater than or equal to.
# lte = less than or equal to.
    start_date = DateFilter(field_name= "date_created", lookup_expr= 'gte')   # inheriting from datefilter and were gona do field names which is a custom input fields.
    end_date = DateFilter(field_name= "date_created", lookup_expr= 'lte')
    note = CharFilter(field_name= 'note', lookup_expr= 'icontains') # here note is model attribute and icontains means ignore case sensitivity.

    class Meta: # we need a minimum of two attributes so the first one is the model that we're gonna be building a filter for & thats gonna be the order model and a fild attributes thats basically saying which fields that we want to allow and for now we want to allow all of them .
        model = Order
        fields = '__all__'
# firstly exclude the customer attribute and the date coz we gonna customize this. make a list of name exclude.
        exclude = ['customer','date_created']
