from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from django.views import View
from myapp.models import Product,Customer,Cart
from django.db.models import Count,Q
from .forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages

# Create your views here.

def home(request):
    return render(request , 'index.html')

def about(request):
    return render(request , 'about.html')


def contact(request):
    return render(request , 'contact.html')


class CategoryView(View):
    def get(self,request,val):
        product= Product.objects.filter(category=val)
        title=Product.objects.filter(category=val).values('title')
        return render(request, "category.html", locals())
    


class ProductDetail(View):
    def get(self,request,pk):
        product= Product.objects.filter(pk=pk)
        return render(request, "productdetail.html", locals())
    


class CategoryTitle(View):
    def get(self,request,val):
        product=Product.objects.filter(title=val)
        title=Product.objects.filter(category=product[0].category).values('title')
        return render(request, "category.html", locals())
    


class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        return render(request, "customerregistration.html", locals())
    
    def post(slef,request):
        form= CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Congratulations! User Register Successfully")
        else:
            messages.warning(request, "Invalid credentials")
        return render(request,'customerregistration.html',locals())
    

class ProfileView(View):
    def get(self,request):
        form= CustomerProfileForm()
        return render(request, "profile.html", locals())
    def post(self,request):
        form= CustomerProfileForm(request.POST)
        if form.is_valid():
            user= request.user
            name= form.cleaned_data['name']
            locality= form.cleaned_data['locality']
            city= form.cleaned_data['city']
            mobile= form.cleaned_data['mobile']
            state= form.cleaned_data['state']
            zipcode= form.cleaned_data['zipcode']

            reg = Customer(user=user,name=name,locality=locality,city=city,mobile=mobile,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request, "Congratulations! Profile Saved Successfully")
        else:
            messages.warning(request, "Invalid credentials")    
        return render(request, "profile.html", locals())
    

def address(request):
    add= Customer.objects.filter(user=request.user)
    return render(request,'address.html', locals())


class UpdateAddress(View):
    def get(self,request,pk):
        add= Customer.objects.get(pk=pk)
        form= CustomerProfileForm(instance=add)
        return render(request,'updateAddress.html', locals())
    def post(self,request,pk):
        form= CustomerProfileForm(request.POST)
        if form.is_valid():
            add= Customer.objects.get(pk=pk)
            add.name= form.cleaned_data['name']
            add.locality= form.cleaned_data['locality']
            add.city= form.cleaned_data['city']
            add.mobile= form.cleaned_data['mobile']
            add.state= form.cleaned_data['state']
            add.zipcode= form.cleaned_data['zipcode']
            add.save()
            messages.success(request, "Congratulations! Profile Updated Successfully")
        else:
            messages.warning(request, "Invalid credentials")

        return redirect('address')
    


def add_to_cart(request):
    user= request.user
    product_id= request.GET.get('prod_id')
    product= Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')


def show_cart(request):
    user=request.user
    cart= Cart.objects.filter(user=user)
    amount= 0
    for p in cart:
        value= p.quantity * p.product.discounted_price
        amount= amount + value
    totalamount=amount + 15
    return render(request, 'addtocart.html',locals())



def plus_cart(request):
    if request.method == 'GET':
        prod_id= request.GET[prod_id]
        c= Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        user= request.user
        cart=Cart.objects.filter(user=user)
        amount= 0
        for p in cart:
            value= p.quantity * p.product.discounted_price
            amount= amount + value
        totalamount= amount + 15
       
        #print(prod_id)
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
    


def plus_cart(request):
    if request.method == 'GET':
        prod_id= request.GET[prod_id]
        c= Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        user= request.user
        cart=Cart.objects.filter(user=user)
        amount= 0
        for p in cart:
            value= p.quantity * p.product.discounted_price
            amount= amount + value
        totalamount= amount + 15       
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)



def remove_cart(request):
    if request.method == 'GET':
        prod_id= request.GET[prod_id]
        c= Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        user= request.user
        cart=Cart.objects.filter(user=user)
        amount= 0
        for p in cart:
            value= p.quantity * p.product.discounted_price
            amount= amount + value
        totalamount= amount + 15
        data={
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
    




class checkout(View):
    def get(self,request):
        user= request.user
        add= Customer.objects.filter(user=user)
        cart= Cart.objects.filter(user=user)
        amount= 0
        for p in cart:
            value= p.quantity * p.product.discounted_price
            amount= amount + value
        totalamount=amount + 15
        return render(request, 'checkout.html', locals())