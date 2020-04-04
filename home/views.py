from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect,get_object_or_404

# Create your views here.

#def homeview(request):
#
#    return render(request,'shop-login.html')
from django.views.generic import DetailView
from django.views.generic.base import View

from home.models import Item, Brand, Ad, Slider, Category, Contactus, OrderItem, Order


class BaseNavView(View):
    template_context = {}

class HomeBaseView(BaseNavView):
    def get(self,request):
        self.template_context['categorys'] = Category.objects.all()
        self.template_context['brands'] = Brand.objects.all()
        self.template_context['indexsale'] = Item.objects.filter(status = 'sale')
        self.template_context['indexhot'] = Item.objects.filter(status = 'hot')
        self.template_context['indexnew'] = Item.objects.filter(status = 'new')
        self.template_context['indexdefault'] = Item.objects.filter(status = 'default')
        self.template_context['ads']= Ad.objects.all()
        self.template_context['sliders'] = Slider.objects.all()
        return render(self.request,'shop-index.html',self.template_context)


#
# def itemdetail(request):
#
#     return render(request,'shop-item.html'

class ItemDetailView(DetailView):
    model = Item
    template_name = 'shop-item.html'

#
# def login(request):
#     return redirect(request, 'accounts/login.html')

def register(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cpassword= request.POST['cpassword']

        if password == cpassword:
            if User.objects.filter(username = username).exists():
                messages.error(request,"This username is already taken")
                return redirect('home:signup')
            if User.objects.filter(email = email).exists():
                messages.error(request, "This email is already taken")
                return redirect('home:signup')
            else:
                user = User.objects.create_user(
                    first_name = first_name,
                    last_name = last_name,
                    username = username,
                    email =  email,
                    password = password
                )
                user.save()

                messages.success(request, "SignUp is Successfull")
                return redirect('/accounts/login')
        else:
            messages.error(request,"Password is not matching")
            return redirect('home:signup')
    else:
        return render(request,'signup.html')
class Search(BaseNavView):


    def get(self,request):
        query = request.GET.get('query')
        if not query:
            return redirect('/')
        else:
            self.template_context['search_item']=Item.objects.filter(title__icontains = query)
        self.template_context['search_item_name'] = query
        return render(request,'shop-search-result.html',self.template_context)

def contactus(request):
    if request.method == "POST":
        first_name=request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        message = request.POST['message']

        contact = Contactus.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            message=message

        )
        contact.save()
        messages.success(request, "Sucessfull")
        return redirect('/contactus/')
    else:
        return render(request,'contactus.html')

def add_to_cart(request,slug):
    item = get_object_or_404(Item,slug = slug)
    order_item = OrderItem.objects.get_or_create(
        item = item,
        user = request.user,
        ordered =False
    )[0]
    orders = Order.objects.filter(
        user = request.user,
        ordered = False
    )
    if orders.exists():
        order = orders[0]
        if order.items.filter(item__slug = item.slug).exists():
            order_item.quantity +=1
            order_item.save()
            messages.success(request,"The quantity is updated")
            return redirect ('/')
        else:
            order.items.add(order_item)
            messages.success(request,"The cart is added")
            return redirect('/')
    else:
        order=Order.objects.create(
            user = request.user
        )
        order.items.add(order_item)
        messages.success(request,"The cart is added")
        return redirect('/')
class OrderSummeryView(BaseNavView):
    def get(self,*args,**kwargs):
        try:
            order = Order.objects.get(
                user = self.request.user,
                ordered = False
            )
            self.template_context['object'] = order
        except:
            return redirect('/')
        return render(self.request,'shop-shopping-cart.html')