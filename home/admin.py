from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Item,Brand,Ad,Slider,Category,Contactus,OrderItem,Order
admin.site.register(Item)
admin.site.register(Brand)
admin.site.register(Ad)
admin.site.register(Slider)
admin.site.register(Category)
admin.site.register(Contactus)
admin.site.register(OrderItem)
admin.site.register(Order)