from django.db import models


# Create your models here.
# this models.py files are simply a python classes that inherit from django models and allow us to create classes that represent database tables here.

class Customer(models.Model):
	name = models.CharField(max_length=200, null=True)
	phone = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200, null=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
    # this will take a snapshot of whenever that model or item was added to the database and hold that and store in this value
# so for this were gonnna do auto_now_add and this just allows us to automatically create that without having
# having to specify when the item is added to the database so were gonna set that to true


	def __str__(self):
		return self.name


class Tag(models.Model):
	name = models.CharField(max_length=200, null=True) # this null true so that this is gonna allow us to make changes to our database & if we ever import data and were not gonna have a name or a customer with name only so were not gonna get any error.

	def __str__(self):
		return self.name

class Product(models.Model):
	CATEGORY = (
			('Indoor', 'Indoor'),
			('Out Door', 'Out Door'),
			)

	name = models.CharField(max_length=200, null=True)
	price = models.FloatField(null=True)  #This field is generally used to store huge floating point numbers in the database.
	category = models.CharField(max_length=200, null=True, choices=CATEGORY)
	description = models.CharField(max_length=200, null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	tags = models.ManyToManyField(Tag)
#(to define a many to many relationship)

	def __str__(self):
		return self.name

class Order(models.Model):
	STATUS = (
			('Pending', 'Pending'),
			('Out for delivery', 'Out for delivery'),
			('Delivered', 'Delivered'),
			)
    # we want customer and pdt to be one to many relationship , we dont wanna have a string value  everysingle time a pdt is ordered ,nor have to manually add in that price or the name so in this case we want to reference a pdt in the store so were not having to put that info and store it within the orders so to create tht relatnship all we need to do is 'models.foreignkey(whatever model we want to be the parent of thismodel )

	customer = models.ForeignKey(Customer, null=True, on_delete= models.SET_NULL)  #what this set.null is gonna do is anytime we remove this order customer for some reason if we delete  them this order will remain in the database just with a no value for customer.
	product = models.ForeignKey(Product, null=True, on_delete= models.SET_NULL)  # the product mntion here after FK is the reference to the pdt.
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	status = models.CharField(max_length=200, null=True, choices=STATUS)

	def __str__(self):
		return self.product.name
