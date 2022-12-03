from django.contrib import admin
from .models import products,category, sub_category,ProductOffer,CategoryOffer,Coupon


# Register your models here.


admin.site.register(products)
admin.site.register(category)
admin.site.register(sub_category)
admin.site.register(ProductOffer)
admin.site.register(CategoryOffer)
admin.site.register(Coupon)
