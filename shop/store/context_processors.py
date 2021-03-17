from django.urls.conf import path
from store.models import Category,Cart,CartItem,Brand
from store.views import _cart_id



def menu_links(request):
    category_links = Category.objects.all().filter()
    brands_links = Brand.objects.all().filter()

    return dict(category_links=category_links, brands_links=brands_links)





def counter(request):
    item_count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            #query cart
            cart= Cart.objects.filter(cart_id = _cart_id(request)) 
            #query cartitem
            cart_Item= CartItem.objects.all().filter(cart=cart[:1])

            for item in cart_Item:
                item_count += item.quantity

        except Cart.DoesNotExist:
            item_count = 0
  
    return  dict(item_count = item_count)