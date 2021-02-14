from django.shortcuts import render, redirect
from store.forms import SignUpForm
from store.models import Category,Product,Banner
from django.contrib.auth.models import Group,User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout , authenticate

# Create your views here.

def index(request):
    products = None
    products = Product.objects.all().filter(available=True)
    banners =  None
    banners  = Banner.objects.all()
   
    return render(request, 'index.html',{'products':products,'banners':banners})
   



def product(request):
    return render(request, 'product.html')

def brand(request):
    return render(request, 'brand.html')   


def signUpView(request):
    if request.method == 'POST':
        form=SignUpForm(request.POST)
        if form.is_valid():
            #บันทึกข้อมูล user
            form.save()
            #บันทึก Group Customer
            #ดึงusername มาใช้
            username = form.cleaned_data.get('username')
            #ดึงข้อมูล user จากฐานข้อมูล
            signUpUser = User.objects.get(username = username)
            #จัด Group
            customer_group = Group.objects.get(name="Customer")
            customer_group.user_set.add(signUpUser)
            return redirect('signIn')

    else :   
        form = SignUpForm()
    return render(request, "signup.html", {'form':form})



def signInView(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username =request.POST['username']
            password =request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return redirect('signUp')

    else:

        form = AuthenticationForm()
    return render(request,'signIn.html', {'form':form})


def signOutView(request):
    logout(request)
    return redirect('signIn')


def search(request):
    products = Product.objects.filter(name__contains = request.GET['title'])
    return render(request,'index.html', {'products':products})