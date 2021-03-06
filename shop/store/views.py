from django.db.models.deletion import SET_NULL
from django.db.models.fields import BLANK_CHOICE_DASH, NullBooleanField
from django.shortcuts import render, redirect, get_object_or_404
from store.forms import SignUpForm
from store.models import Category,Brand,Product,Banner,Cart,CartItem,Order,OrderItem
from django.contrib.auth.models import Group,User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout , authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator,EmptyPage,InvalidPage

# Create your views here.

def index(request):
    products = None
   
    banners =  None
    banners  = Banner.objects.all()

  
    products = Product.objects.all().filter(available=True)
   
    return render(request, 'index.html',{'products':products,'banners':banners,})
   


def product_by_category(request,category_slug=None,subcategory_slug=None):
    products = None
    category_page = None

    if subcategory_slug == None :  # parent
        category_page = get_object_or_404(Category, slug=category_slug )
        products = Product.objects.all().filter(category__parent = category_page , available=True)

     
    else:
        category_page = get_object_or_404(Category, parent__slug=category_slug , slug = subcategory_slug )
        products = Product.objects.all().filter(category=category_page, available=True)
   


    paginator = Paginator(products,2)
    try:
        page=int(request.GET.get('page','1'))
    except:
        page=1

    try: 
        productperPage = paginator.page(page)
    except (EmptyPage,InvalidPage):
        productperPage = paginator.page(paginator.num_pages)
        


    return render(request, 'products.html',{'products':productperPage,'category':category_page})
   

def product_by_brand(request,brand_slug=None):
    products = None
    brand_page = None

    
    brand_page = get_object_or_404(Brand, slug= brand_slug )
    products = Product.objects.all().filter(brand = brand_page , available=True)

    paginator = Paginator(products,2)
    try:
        page=int(request.GET.get('page','1'))
    except:
        page=1

    try: 
        productperPage = paginator.page(page)
    except (EmptyPage,InvalidPage):
        productperPage = paginator.page(paginator.num_pages)

    return render(request, 'products.html',{'products':productperPage,'brand':brand_page})




def productPage(request,category_slug,subcategory_slug,product_id):
    try:
        
        product = Product.objects.get(category__parent__slug = category_slug ,category__slug= subcategory_slug , id=product_id )
    except Exception as e :
        raise e

    return render(request, 'productdetail.html',{'product':product})



def _cart_id(request):
    cart = request.session.session_key
    if not cart :
        cart = request.session.create()
    return cart



@login_required(login_url='signIn')
def addCart(request,product_id):
    
    if request.method == 'POST':

             
        quantity  = request.POST['number']

        #ดึงสินค้าที่จะซื้อ
        product = Product.objects.get(id=product_id)

        if int(quantity) < product.stock : #สินค้ามีstock พอให้ซื้อ
      
            #สร้างตะกร้า
            try:
                cart=Cart.objects.get(cart_id=_cart_id(request))
            except Cart.DoesNotExist :
                cart=Cart.objects.create(cart_id=_cart_id(request))
                cart.save()

            try:
                #ซื้อรายการสินค้าซ้ำ
                cart_item=CartItem.objects.get(product=product, cart=cart)
                if cart_item.quantity < cart_item.product.stock:
                    #เปลี่ยนจำนวนรายการสินค้า
                    cart_item.quantity+= int(quantity)
                    cart_item.save()
            except CartItem.DoesNotExist :
                #ซื้อรายการสินค้าครั้งแรก
                #บันทึกลงDB
                cart_item=CartItem.objects.create(
                    product = product,
                    cart = cart,
                    quantity = quantity
                    )
                cart_item.save()
        
        else:
            return redirect('home')
            


    return redirect('/')



def cartdetail(request):
    total = 0
    counter =0
    cart_items = None
    try:
        cart =Cart.objects.get(cart_id=_cart_id(request)) #ดึงตะกร้า
        cart_items =CartItem.objects.filter(cart=cart, active=True) #ดึงข้อมูลสินค้าในตะกร้า
        for item in cart_items:
            total+=(item.product.price*item.quantity)
            counter+=(item.quantity)
    except Exception as e:
        pass

    return render(request, 'cartdetail.html', dict(cart_items=cart_items, total=total, counter=counter))



def removeCart(request, product_id):
    cart= Cart.objects.get(cart_id = _cart_id(request))
    product= get_object_or_404(Product, id =product_id)
    cartItem = CartItem.objects.get(product=product, cart=cart)
    cartItem.delete()

    return redirect('cartDetail')



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
    return render(request,'products.html', {'products':products})


def orderHistory(request):
    if request.user.is_authenticated:
        email = str(request.user.email)
        orders = Order.objects.filter(email=email)
    return render(request, 'order.html', {orders:orders})