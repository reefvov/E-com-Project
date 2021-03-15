from django.contrib import admin
from store.models import Category,Brand,Product,Banner,Cart,CartItem,Coupon,Order,OrderItem

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display =['name','price','stock','created','updated']
    list_editable =['price','stock']
    list_per_page = 20
    search_fields = ['name']


class CouponAdmin(admin.ModelAdmin):
     list_display =['code', 'valid_from', 'valid_to', 'discount', 'active']
     list_filter = ['active', 'valid_from' , 'valid_to' ]
     list_editable =['active']
     search_fields = ['code']


class OrderItemline(admin.TabularInline):
    model = OrderItem
    list_display =['order','product','price','quantity','amount']
    extra = 0

class OrderItemAdmin(admin.ModelAdmin):
    list_display =['order','product','price','quantity']
    list_filter = ['order']

class OrderAdmin(admin.ModelAdmin):
    list_display =['id','order_no','total','created','updated','slip','status']
    list_editable =['status']
    inlines = [OrderItemline]



admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Product,ProductAdmin)
admin.site.register(Banner)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Coupon, CouponAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderItem,OrderItemAdmin)