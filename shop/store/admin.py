from django.contrib import admin
from store.models import Category,Brand,Product,Banner,Cart,CartItem

# Register your models here.

class PruductAdmin(admin.ModelAdmin):
    list_display =['name','price','stock','created','updated']
    list_editable =['price','stock']
    list_per_page = 10




admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Product,PruductAdmin)
admin.site.register(Banner)
admin.site.register(Cart)
admin.site.register(CartItem)