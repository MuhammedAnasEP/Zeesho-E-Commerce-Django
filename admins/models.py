from django.db import models

# Create your models here.

class category(models.Model):
    category_name=models.CharField(max_length=50)
    cat_image = models.ImageField(upload_to ='photo')
    offer=models.IntegerField(default=0)

    def __str__(self) :
        return self.category_name



class sub_category(models.Model):
    name = models.CharField(max_length = 50)
    image = models.ImageField(upload_to = 'photo')
    Main_category=models.ForeignKey(category, on_delete = models.CASCADE)

    def __str__(self) :
        return self.name



class products(models.Model):
    product_name=models.CharField(max_length=50)
    price=models.FloatField()
    Category=models.ForeignKey(category, on_delete = models.CASCADE)
    sub_category=models.ForeignKey(sub_category, on_delete = models.CASCADE)
    image = models.ImageField(upload_to ='photo')
    image1 = models.ImageField(upload_to ='photo',default=0)
    image2 = models.ImageField(upload_to ='photo',default=0, null = True)
    image3 = models.ImageField(upload_to ='photo',default=0, null = True)
    image4 = models.ImageField(upload_to ='photo',default=0, null = True)
    
    size=models.CharField(max_length=20)
    stock=models.IntegerField()
    description=models.CharField(max_length=200)
    p_offer=models.IntegerField(default=0)
    p_offer_price=models.IntegerField(default=0)
    c_offer=models.IntegerField(default=0)
    c_offer_price=models.IntegerField(default=0)
    
    def __str__(self) :
        return self.product_name

# class Products_image(models.Model):
#     Products = models.ForeignKey(products,on_delete = models.CASCADE)
#     image_files = models.ImageField(upload_to = 'photo') 


class ProductOffer(models.Model):
    product = models.ForeignKey(products, on_delete=models.CASCADE, null=True, blank=True)
    offer = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

class CategoryOffer(models.Model):
    category = models.ForeignKey(category, on_delete=models.CASCADE, null=True, blank=True)
    offer = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

class Coupon(models.Model):
    code = models.CharField(max_length=50)
    discount_amount = models.IntegerField()
    start_date = models.DateField()
    min_amount = models.IntegerField(default=0)
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code