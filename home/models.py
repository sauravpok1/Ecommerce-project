

# Create your models here.
from django.db import models
from django.urls import reverse
from django.conf import settings

STATUS=(('active','active'),('','default'))
STATUSS = (('sale','sale'),('hot','hot'),('new','new'),('','default'))
STOCK = (('In Stock','In Stock'),('Out Of Stock','Out Of Stock'))

class Category(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    image = models.TextField()

    def __str__(self):
        return self.name



class Item(models.Model):
    title = models.CharField(max_length=200)
    price = models.FloatField()
    discounted_price = models.FloatField(blank = True)
    image = models.TextField()
    description = models.TextField()
    slug = models.CharField(max_length=200)
    brand = models.CharField(max_length=200,blank = True)
    status = models.CharField(max_length=100,choices=STATUSS,blank=True)
    stock = models.CharField(choices=STOCK,max_length = 50,blank=True)
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse("home:product",kwargs={'slug':self.slug})
    def get_add_to_cart(self):
        return reverse("home:add-to-cart",kwargs={'slug':self.slug})

class Brand(models.Model):
    name = models.CharField(max_length=200)
    image = models.TextField()
    description = models.TextField()
    def __str__(self):
        return self.name

class Ad(models.Model):
    name=models.CharField(max_length=200)
    rank=models.IntegerField()
    status=models.CharField(choices=STATUS,max_length=100,blank = True)
    image=models.TextField()
    description = models.TextField()

    def __str__(self):
        return self.name

class Slider(models.Model):
    name = models.CharField(max_length=200)
    rank = models.IntegerField()
    status = models.CharField(choices=STATUS, max_length=100, blank=True)
    image = models.TextField()
    description = models.TextField()
    Text_one = models.TextField()
    Text_two = models.TextField()
    Text_three = models.TextField()
    url = models.TextField()

    def __str__(self):
        return self.name

class Contactus(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=300)
    username=models.CharField(max_length=300)
    email = models.CharField(choices=STATUS, max_length=100, blank=True)
    message = models.CharField(choices=STATUS, max_length=100, blank=True)
class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    item = models.ForeignKey(Item,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)
    def __str__(self):
        return self.item.title
    def get_total_price(self):
        return self.quantity*self.item.price
    def get_total_discounted_price(self):
        return self.quantity*self.item.discounted_price
    def get_total_sum_price(self):
        if self.item.discount_price:
            return self.get_item_discounted_price()
        else:
            return self.get_total_price()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items=models.ManyToManyField(OrderItem)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total_price = 0
        for orders in self.item.all():
            total_price += orders.get_total_sum_price()
        return total_price
    def get_all_total_price(self):
        all_total = self.get_total() + 10
        return all_total

