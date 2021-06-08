# we'll create a form in here and what we're gonna use is something called a model form and this is just a python way of actually building out our forms and it makes everything really easy to add in a form into a template and we prcess and save that data .

from django.forms import ModelForm
from .models import Order

class OrderForm(ModelForm): # inheriting from ModelForm.
        class Meta:        # we'll need to specify two fields.
            model = Order  # it needs to know which model are we gonna build a form for.
            fields = '__all__' # fields which we gonna allow.

# __all__ create a form with all of these fields in it.
# if we wanted to use one field i would actually just do a list here , ex: fields = ['customer','product']
