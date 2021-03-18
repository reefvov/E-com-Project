from django.db.models.deletion import SET_NULL
from django.db.models.fields import BLANK_CHOICE_DASH, NullBooleanField
from django.shortcuts import render, redirect, get_object_or_404
from store.forms import SignUpForm,CouponApplyForm,CheckOutForm,PaymentForm
from store.models import Category,Brand,Product,Banner,Cart,CartItem,Order,OrderItem,Coupon
from django.contrib.auth.models import Group,User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout , authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator,EmptyPage,InvalidPage
from django.utils import timezone
from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse

# Create your views here.

def index(request):
    products = None
   
    banners =  None
    banners  = Banner.objects.all()

  
    products = Product.objects.all().filter(available=True)[:10]
    products_lastest = Product.objects.all().order_by('-id')[:10]
    category = Category.objects.all()
    brands = Brand.objects.all()
   
    return render(request, 'index.html',{'products':products,'banners':banners,'catagory':category,
                                        'products_lastest': products_lastest, 'brands':brands })
   


def product_by_category(request,category_slug=None):
    products = None
    category_page = None

    category_page = get_object_or_404(Category, slug=category_slug )

    catagory_ancestor = category_page.get_ancestors(ascending=False, include_self=True)

    if category_page.is_leaf_node() == True :  # parent
        products = Product.objects.all().filter(category = category_page , available=True)

     
    else:
        products =  Product.objects.none()
        category_set = category_page.get_descendants(include_self=False)
        for cat in category_set :
         
            if cat.is_leaf_node() == True:
               
                products_ = Product.objects.all().filter(category=cat, available=True)
                products = products.union(products_)
                print(products)
                
            else: 
             
                continue


    paginator = Paginator(products.order_by('id'),3)
    try:
        page=int(request.GET.get('page','1'))
    except:
        page=1

    try: 
        productperPage = paginator.page(page)
    except (EmptyPage,InvalidPage):
        productperPage = paginator.page(paginator.num_pages)
        


    return render(request, 'products.html',{'products':productperPage,'category':category_page, 'catagory_ancestor':catagory_ancestor })
   

def product_by_brand(request,brand_slug=None):
    products = None
    brand_page = None

    
    brand_page = get_object_or_404(Brand, slug= brand_slug )
    products = Product.objects.all().filter(brand = brand_page , available=True)

    paginator = Paginator(products.order_by('id'),3)
    try:
        page=int(request.GET.get('page','1'))
    except:
        page=1

    try: 
        productperPage = paginator.page(page)
    except (EmptyPage,InvalidPage):
        productperPage = paginator.page(paginator.num_pages)

    return render(request, 'products.html',{'products':productperPage,'brand':brand_page})




def productPage(request,product_id):
    try:
        
        product = Product.objects.get( id=product_id )
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

        if int(quantity) <= product.stock : #สินค้ามีstock พอให้ซื้อ
      
            #สร้างตะกร้า
            try:
                cart=Cart.objects.get(cart_id=_cart_id(request))
            except Cart.DoesNotExist :
                cart=Cart.objects.create(cart_id=_cart_id(request))
                cart.save()

            try:
                #ซื้อรายการสินค้าซ้ำ
                cart_item=CartItem.objects.get(product=product, cart=cart)
                if int(quantity) <= cart_item.product.stock - cart_item.quantity:

                    #เปลี่ยนจำนวนรายการสินค้า
                    cart_item.quantity+= int(quantity)
                    cart_item.save()
                else:
                    print('ssssssssssssssssssssssssssssssssssssss')
                    messages.error(request,'จำนวนสินค้ามีไม่พอ')
                    return  redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
            except CartItem.DoesNotExist :
                #ซื้อรายการสินค้าครั้งแรก
                #บันทึกลงDB
                cart_item=CartItem.objects.create(
                    product = product,
                    cart = cart,
                    quantity = quantity
                    )
                cart_item.save()
                print('quantity = ',quantity)
        
        else:
            messages.error(request,'จำนวนสินค้ามีไม่พอ')
            return  redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
            


    return  redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))



def cartdetail(request):
    total = 0
    counter =0
    cart_items = None
    discount_price = None
    new_total= None
    coupon = None
    coupon_id = 0
    add_coupon = False


    try:
        cart =Cart.objects.get(cart_id=_cart_id(request)) #ดึงตะกร้า
        cart_items =CartItem.objects.filter(cart=cart, active=True) #ดึงข้อมูลสินค้าในตะกร้า
        for item in cart_items:
            total+=(item.product.price*item.quantity)
            counter+=(item.quantity)
    except Exception as e:
        pass
    


    if request.method == 'POST':

        if 'redeem' in request.POST:

            now = timezone.now()
            form = CouponApplyForm(request.POST)
            if form.is_valid():
                code = form.cleaned_data.get('code')
                
                try:
                    coupon = Coupon.objects.get(code__iexact = code,
                                                valid_from__lte = now,
                                                valid_to__gte = now,
                                                active = True)

                    if total >= coupon.minimum:
                        add_coupon = True
                        new_total = total - coupon.discount
                        coupon_id = coupon.id
                        
                        
                    else:
                        add_coupon = False
                        new_total= total
                        messages.error(request,'ราคาของสินค้าไม่ถึงราคาขั้นต่ำที่กำหนดไว้')
                        form = CouponApplyForm()
                        #return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

                except Coupon.DoesNotExist:
                    messages.error(request,'ไม่พบคูปอง หรือ หมดอายุ')
                    new_total= total
                    add_coupon = False
                    

    else:
        form = CouponApplyForm()
        new_total = total
        

    return render(request, 'cartdetail.html', dict(cart_items=cart_items, total=total, 
                                                    counter=counter, new_total=new_total, add_coupon=add_coupon,
                                                   coupon=coupon, form=form, coupon_id=coupon_id))





def removeCoupon(request):
    add_coupon = False
    return redirect('cartDetail')


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

    

def checkOutView(request,coupon_id):
    total = 0
    counter = 0
    cart_items = None
    discount_price = None
    new_total= None
    add_coupon = False
    coupon = None
    

    try:
        cart =Cart.objects.get(cart_id=_cart_id(request)) #ดึงตะกร้า
        cart_items =CartItem.objects.filter(cart=cart, active=True) #ดึงข้อมูลสินค้าในตะกร้า
        for item in cart_items:
            total+=(item.product.price*item.quantity)
            counter+=(item.quantity)
    except Exception as e:
        pass

    form = CheckOutForm(request.POST)

    

    if request.method == 'POST': 
        
        if 'confirm' in request.POST:
            print('Uppppppppppppppppppppppppppppppppp')
            if coupon_id == 0:
                new_total = total

            else:
                coupon = Coupon.objects.get(id=coupon_id)
                new_total = total - coupon.discount
                add_coupon = True


        else:
            print('Downnnnnnnnnnnnnnnnnnnnnnnnnnnnnn')
            if coupon_id == 0:
                new_total = total

            else:
                coupon = Coupon.objects.get(id=coupon_id)
                new_total = total - coupon.discount
                add_coupon = True
            form = CheckOutForm(request.POST)
            if form.is_valid():
                now = timezone.now()
                data = Order()

                data.first_name = form.cleaned_data['first_name']
                data.last_name = form.cleaned_data['last_name']
                data.phone = form.cleaned_data['phone']
                data.user_id = request.user.username
                data.address = form.cleaned_data.get('address')
                data.city = form.cleaned_data.get('city')
                data.district = form.cleaned_data.get('district')
                data.subdistrict = form.cleaned_data.get('subdistrict')
                data.postcode = form.cleaned_data.get('postcode')
                data.total = new_total
                data.status =  'รอชำระเงิน'
                if coupon_id != 0:
                    data.code = coupon.code
                data.save()
                
             

                for item in cart_items:
                    order_item = OrderItem.objects.create(
                        product = item.product.name,
                        quantity = item.quantity,
                        price = item.product.price,
                        order = data
                    )
                    order_item.save()
                    #ลดจำนวนstock
                    product = Product.objects.get(id = item.product.id)
                    product.stock = int(item.product.stock - order_item.quantity)
                    product.save()
                    item.delete()
                order = Order.objects.get(id=data.id)
                return redirect(order.get_url())

    else:   
        form = CheckOutForm()
        new_total = total
        
    return render(request, "checkout.html", dict(cart_items=cart_items, total=total, counter=counter,form=form 
                                                 , new_total= new_total ,coupon= coupon , add_coupon= add_coupon,
                                                 coupon_id = coupon_id ))



def paymentView(request,order_id):
    
    if request.method == 'POST' :
        form = PaymentForm(request.POST,request.FILES)
        if form.is_valid():
            order = Order.objects.get(id=order_id)
            order.slip = form.cleaned_data['slip']
            order.status = 'ชำระเงินแล้ว-รอตรวจสอบ'
            order.save()
        return redirect('/')
    else :   
        form = PaymentForm()
        order = Order.objects.get(id=order_id)
        total = order.total


    return render(request,'payment.html',dict(form=form, order_id=order_id, total=total))



def orderHistory(request):
    if request.user.is_authenticated:
        username = str(request.user.username)
        orders = Order.objects.filter(user_id=username)


    paginator = Paginator(orders.order_by('-id'),10)
    try:
        page=int(request.GET.get('page','1'))
    except:
        page=1

    try: 
        orderperPage = paginator.page(page)
    except (EmptyPage,InvalidPage):
        orderperPage = paginator.page(paginator.num_pages)
    return render(request, 'order.html', {'orders':orderperPage})




def viewOrder(request,order_id):
    coupon = None
    if request.user.is_authenticated:
        username = str(request.user.username)
        order = Order.objects.get(user_id=username,id=order_id)
        orderitem = OrderItem.objects.filter(order=order)
        try:
            coupon = Coupon.objects.get(code=order.code)
            if  coupon == None:
                coupon = None
               
        except Coupon.DoesNotExist:
            pass

    return render(request, 'viewOrder.html', {'order':order, 'order_item':orderitem, 'coupon':coupon})



def search(request):
    title = request.GET.get('title')
    products = Product.objects.none()
    products_name = Product.objects.filter(name__icontains = request.GET.get('title', None) , available=True)
    products_category = Product.objects.filter(category__name__icontains = request.GET.get('title') , available=True)
    products_brand = Product.objects.filter(brand__name__icontains = request.GET.get('title') , available=True)
    products = products.union(products_name)
    products = products.union(products_category)
    products = products.union(products_brand)



    paginator = Paginator(products.order_by('id'),2)
    try:
        page=int(request.GET.get('page','1'))
    except:
        page=1

    try: 
        productperPage = paginator.page(page)
    except (EmptyPage,InvalidPage):
        productperPage = paginator.page(paginator.num_pages)

    return render(request, 'products.html',{'products':productperPage, 'title':title})

    
    