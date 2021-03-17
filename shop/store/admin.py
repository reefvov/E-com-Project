from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from store.models import Category,Brand,Product,Banner,Cart,CartItem,Coupon,Order,OrderItem

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display =['name','price','stock','created','updated']
    list_editable =['price','stock']
    list_per_page = 20
    search_fields = ['name','id']
  


class BrandAdmin(admin.ModelAdmin):
    list_display =['name']
    list_per_page = 20
    search_fields = ['name']
  
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
class CouponAdmin(admin.ModelAdmin):
     list_display =['code', 'valid_from', 'valid_to', 'discount', 'active']
     list_filter = ['active', 'valid_from' , 'valid_to' ]
     list_editable =['active']
     search_fields = ['code']
     list_per_page = 20


class OrderItemline(admin.TabularInline):
    model = OrderItem
    list_display =['order','product','price','quantity','amount']
    extra = 0


class OrderItemAdmin(admin.ModelAdmin):
    list_display =['order','product','price','quantity']
    list_filter = ['order']


class OrderAdmin(admin.ModelAdmin):
    list_display =['id','total','created','updated','slip','status']
    list_editable =['status']
    list_filter = ['status']
    search_fields = ['id']
    inlines = [OrderItemline]


class CategoryAdmin(DraggableMPTTAdmin):
    mptt_indent_field = 'name'
    list_display = ('tree_actions', 'indented_title',
                    'related_products_count', 'related_products_cumulative_count')
    list_display_links = ('indented_title',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
                qs,
                Product,
                'category',
                'products_cumulative_count',
                cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                 Product,
                 'category',
                 'products_count',
                 cumulative=False)
        return qs

    def related_products_count(self, instance):
        return instance.products_count
    related_products_count.short_description = 'Related products (for this specific category)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count
    related_products_cumulative_count.short_description = 'Related products (in tree)'



admin.site.register(Category,CategoryAdmin)
admin.site.register(Brand)
admin.site.register(Product,ProductAdmin)
admin.site.register(Banner)
#admin.site.register(Cart)
#admin.site.register(CartItem)
admin.site.register(Coupon, CouponAdmin)
admin.site.register(Order,OrderAdmin)
#admin.site.register(OrderItem,OrderItemAdmin)