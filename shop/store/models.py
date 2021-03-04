from django.db import models
from django.db.models.deletion import CASCADE
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    parent = models.ForeignKey('self',blank=True, null=True,related_name='children',on_delete=CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField() #ใช้ตั้งชื่อเล่นให้ข้อมูลในmodel
    
    class Meta:
        unique_together = ('slug','parent',)
        verbose_name = 'หมวดหมู่'
        verbose_name_plural = "ข้อมูลประเภทสินค้า"

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent

        return ' -> '.join(full_path[::-1])
    
    def get_url(self):
        if self.parent == None:
            return reverse('product_by_category', args=[self.slug])
        else:
            return reverse('product_by_subcategory', args=[self.parent.slug, self.slug])
        


class Brand(models.Model):
    name = models.CharField(max_length=255,unique=True)
    slug = models.SlugField(max_length=255,unique=True) #ใช้ตั้งชื่อเล่นให้ข้อมูลในmodel
    image = models.ImageField(upload_to="brand",blank=True)

    def __str__(self) :
        return self.name  

    class Meta:
        verbose_name = 'แบรนด์สินค้า'
        verbose_name_plural = "ข้อมูลแบรนด์สินค้า"
     
    def get_url(self):
        return reverse('product_by_brand', args=[self.slug])

        
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, blank=True, null=True,on_delete=CASCADE)
    brand = models.ForeignKey(Brand,on_delete= models.CASCADE)
    unit = models.CharField(max_length=255)
    image = models.ImageField(upload_to="product",blank=True)
    stock =  models.IntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) :
        return self.name

    def get_cat_list(self):
        k = self.category
        breadcrumb = ["dummy"]
        while k is not None:
            breadcrumb.append(k.slug)
            k = k.parent
            
        
        for i in range(len(breadcrumb)-1):
            breadcrumb[i] = '/'.join(breadcrumb[-1:i-1:-1])
        return breadcrumb[-1:0:-1]


    class Meta:
        verbose_name = 'สินค้า'
        verbose_name_plural = "ข้อมูลสินค้า"

    def get_url(self):
        return reverse('productDetail', args=[self.category.parent.slug,self.category.slug, self.id])



class Banner(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="banner",blank=True)
    url = models.URLField(max_length = 200)

    def __str__(self) :
        return self.name

    class Meta:
        verbose_name = 'ประกาศ'
        verbose_name_plural = "ประกาศ"

    
class Cart(models.Model):
    cart_id = models.CharField(max_length=255,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return self.cart_id

    class Meta:
        db_table = 'cart'
        ordering = ('date_added',)
        verbose_name = 'ตะกร้าสินค้า'
        verbose_name_plural = "ข้อมูลตะกร้าสินค้า"
        

class CartItem(models.Model):
    product = models.ForeignKey(Product,on_delete=CASCADE)
    cart = models.ForeignKey(Cart,on_delete=CASCADE)
    quantity = models.IntegerField()
    active = models.BooleanField(default=True)

    def __str__(self) :
            return self.product.name

    class Meta:
        db_table = 'cartItem'
        verbose_name = 'รายการสินค้าในตะกร้า'
        verbose_name_plural = "ข้อมูลรายการสินค้าในตะกร้า"

    def sub_total(self):
        return    self.product.price * self.quantity 
    

class Order(models.Model):
    name = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    postcode = models.CharField(max_length=255, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    email = models.EmailField(max_length=255, blank=True)
    token = models.CharField(max_length=255, blank=True)

    def __str__(self) :
            return str(self.id)


    class Meta :
         db_table = 'Order'

    

class OrderItem(models.Model):
    product = models.CharField(max_length=255)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    order = models.ForeignKey(Order,on_delete=CASCADE)

    def sub_total(self) :
            return self.quantity*self.price

    class Meta :
         db_table = 'OrderItem'

    def __str__(self) :
            return self.product

