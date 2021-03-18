"""shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from store import views
from django.conf.urls.static import static
from django.conf import settings


   

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('category/<slug:category_slug>', views.product_by_category, name="product_by_category"),
    path('product/<int:product_id>', views.productPage, name='productDetail'),
    path('brand/<slug:brand_slug>',views.product_by_brand ,name='product_by_brand'),
    path('cart/add/<int:product_id>', views.addCart, name='addCart'),
    path('cart/remove/<int:product_id>', views.removeCart, name='removeCart'),
    path('cartdetail/', views.cartdetail,name='cartDetail'),
    path('removeCoupon/', views.removeCoupon, name='removeCoupon'),
    path('checkout/', views.checkOutView, name='checkOut'),
    path('checkout/<int:coupon_id>', views.checkOutView, name='checkOut'),
    path('payment/<int:order_id>', views.paymentView, name='payment'),
    path('account/create', views.signUpView, name='signUp' ),
    path('account/login', views.signInView, name='signIn' ),
    path('account/logout', views.signOutView, name='signOut' ),
    path('search/', views.search, name='search' ),
    path('orderHistory/', views.orderHistory, name='orderHistory'),
    path('order/<int:order_id>', views.viewOrder, name='orderDetail' ),
    path('thankyou/', views.thankyou, name='thankyou' )

]

if settings.DEBUG :
    #/media/product
    urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
    #/static/
    urlpatterns += static(settings.STATIC_URL,document_root = settings.STATIC_ROOT)
    #static/media/product/xxx.jpg