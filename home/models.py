from crypt import methods
from email.policy import default
from django.db import models
from members.models import CustomUser
from admins.models import products
# Create your models here.


class Cart(models.Model):

    user = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    product = models.ForeignKey(products, on_delete = models.CASCADE)
    ordered = models.BooleanField(default = False)
    quantity = models.IntegerField(default = 1)
    
    
    def get_total_item_price(self):
        if self.product.p_offer_price < 1 and self.product.c_offer_price < 1:
            return self.quantity * self.product.price
        elif self.product.p_offer_price > 1 and self.product.c_offer_price < 1:
            return self.quantity * self.product.p_offer_price
        elif self.product.p_offer_price < 1 and self.product.c_offer_price > 1:
            return self.quantity * self.product.c_offer_price
        elif self.product.p_offer_price > self.product.c_offer_price and self.product.c_offer_price > 1:
            return self.quantity * self.product.c_offer_price
        elif self.product.p_offer_price < self.product.c_offer_price and self.product.p_offer_price > 1:
            return self.quantity * self.product.p_offer_price
        elif self.product.p_offer_price == self.product.c_offer_price and self.product.p_offer_price > 1 and self.product.c_offer_price > 1:
            return self.quantity * self.product.c_offer_price
    def get_final_price(self):
        return self.get_total_item_price()

class Address(models.Model):
    user = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    type = models.CharField(max_length = 100)
    name =models.CharField(max_length=100)
    address = models.CharField(max_length = 200)
    district = models.CharField(max_length = 100)
    state = models.CharField(max_length = 100)
    pin_code =models.CharField(max_length = 100)
    contact_number = models.BigIntegerField()
    additional_number = models.BigIntegerField()
    

class Order(models.Model):
    user = models.ForeignKey(CustomUser,on_delete = models.CASCADE)
    ordered_date = models.DateTimeField(auto_now_add = True)
    ordered = models.BooleanField(default = False)
    address = models.ForeignKey(Address,on_delete = models.CASCADE)
    product = models.ForeignKey(products, on_delete = models.CASCADE)
    method = models.CharField(max_length = 100,default='cash on delivery')
    amount = models.FloatField(default=0)
    quantity = models.IntegerField(default = 1)
    status = models.CharField(max_length=100, default='Confirmed')
    coupon_code = models.CharField(max_length=100,blank=True)
    discounted_amnt = models.FloatField(default=0.0)
    def get_total_item_price(self):
        if self.product.p_offer_price < 1 and self.product.c_offer_price < 1:
            return self.quantity * self.product.price
        elif self.product.p_offer_price > 1 and self.product.c_offer_price < 1:
            return self.quantity * self.product.p_offer_price
        elif self.product.p_offer_price < 1 and self.product.c_offer_price > 1:
            return self.quantity * self.product.c_offer_price
        elif self.product.p_offer_price > self.product.c_offer_price and self.product.c_offer_price > 1:
            return self.quantity * self.product.c_offer_price
        elif self.product.p_offer_price < self.product.c_offer_price and self.product.p_offer_price > 1:
            return self.quantity * self.product.p_offer_price
        elif self.product.p_offer_price == self.product.c_offer_price and self.product.p_offer_price > 1 and self.product.c_offer_price > 1:
            return self.quantity * self.product.c_offer_price

    def get_final_price(self):
        return self.get_total_item_price()




class Wishlist(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(products, on_delete=models.CASCADE)

