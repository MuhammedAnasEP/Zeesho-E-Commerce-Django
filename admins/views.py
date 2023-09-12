from ctypes.wintypes import DWORD
from email.mime import image
from nis import cat
from urllib import request
from django.shortcuts import render, redirect
from django.contrib.auth.models import auth, User
from members.models import CustomUser
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import products, category, sub_category, ProductOffer, CategoryOffer, Coupon
from django.views.decorators.cache import never_cache
from home.models import Order
import math
# Create your views here.
User = get_user_model()


@never_cache
def admins_log(request):
    if request.user.is_superuser:
        return redirect(admins_home)
    return render(request, 'admins_login.html')


@never_cache
def admins_home(request):
    if request.user.is_superuser:
        if 's' in request.POST:
            s = request.POST['s']
            details = User.objects.filter(username__icontains=s)
        else:
            details = User.objects.all()
        return render(request, 'admins_home.html', {'details': details})
    return redirect(admins_log)


@never_cache
def admins_login(request):
    if request.user.is_superuser:
        return redirect(admins_home)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None and user.is_superuser:
            auth.login(request, user)
            return redirect(admins_home)
        else:
            messages.info(request, 'User Name Not Valid')
            return redirect(admins_log)
    else:
        return render(request, 'admins_login.html')


@never_cache
def admins_logout(request):
    if request.user.is_superuser:
        auth.logout(request)
    return redirect(admins_login)


def product_details(request):
    if request.user.is_superuser:
        if 's' in request.POST:
            s = request.POST['s']
            product_details = User.objects.filter(product_name__icontains=s)
        else:
            product_details = products.objects.all()
        return render(request, 'product_details.html', {'details': product_details})
    return redirect(admins_log)


def add_products(request):
    cat = category.objects.all()
    sub_cat = sub_category.objects.all()
    return render(request, 'add_products.html', {"cat": cat, "sub_cat": sub_cat})


def new_products(request):
    if request.method == 'POST':
        product_name = request.POST['name']
        price = request.POST.get('price')
        cat1 = request.POST.get('category')
        print(cat1)
        try:
            cat = category.objects.get(id=cat1)
        except:
            return redirect(add_products)
        img = request.FILES['image']
        img1 = request.FILES.get('image1',0)
        img2 = request.FILES.get('image2',0)
        img3 = request.FILES.get('image3',0)
        img4 = request.FILES.get('image4',0)

        sub_cat1 = request.POST.get('sub_category')
        print(sub_cat1)
        try:
            sub_cat = sub_category.objects.get(id=sub_cat1)
        except:
            return redirect(add_products)
        size = request.POST['size']
        stock = request.POST['stock']
        description = request.POST['description']

        prod = products.objects.create(
            product_name=product_name, price=price, Category=cat, image=img, image1=img1, image2=img2, image3=img3, image4=img4, sub_category=sub_cat, size=size, stock=stock, description=description)
        prod.save()

        # if request.FILES.get('image_files')!=0:
        #     images = request.FILES.get('image_files')
        #     for img in images:
        #         image = Products_image.objects.create(Products = prod, image_files = img)
        #         image.save()

        return redirect(product_details)


def edit_products(request, id):
    if request.user.is_authenticated:
        prod = products.objects.get(id=id)
        cat = category.objects.all()
        sub_cat = sub_category.objects.all()
        return render(request, 'products_edit.html', {'prod': prod, "cat": cat, "sub_cat": sub_cat})

    return redirect(product_details)


def pro_update(request, id):
    if request.method == 'POST':
        prod = products.objects.get(id=id)
        product_name = request.POST['name']
        price = request.POST['price']
        cat1 = request.POST.get('category')
        print(cat1)
        try:
            cat = category.objects.get(id=cat1)
        except:
            return redirect(edit_products)

        img = request.FILES.get('image', prod.image)
        img1 = request.FILES.get('image1', prod.image1)
        img2 = request.FILES.get('image2', prod.image2)
        img3 = request.FILES.get('image3', prod.image3)
        img4 = request.FILES.get('image4', prod.image4)

        sub_cat1 = request.POST.get('sub_category')
        print(sub_cat1)
        try:
            sub_cat1 = sub_category.objects.get(id=sub_cat1)
        except:
            return redirect(edit_products)

        size = request.POST['size']
        stock = request.POST['stock']
        description = request.POST['description']

        prod.product_name = product_name
        prod.price = price
        prod.Category = cat
        prod.image = img
        prod.image1 = img1
        prod.image2 = img2
        prod.image3 = img3
        prod.image4 = img4
        prod.sub_category = sub_cat1
        prod.size = size
        prod.stock = stock
        prod.description = description
        prod.save()

        return redirect(product_details)


def product_delete(request, id):
    prod_del = products.objects.get(id=id)

    prod_del.delete()
    return redirect(product_details)


def categorys(request):
    if request.user.is_superuser:
        if 's' in request.POST:
            s = request.POST['s']
            cat = category.objects.filter(category_name__icontains=s)
        else:
            cat = category.objects.all()
            subcat = sub_category.objects.all()
        return render(request, 'categorys.html', {'details': cat, 'subcat': subcat})
    return redirect(admins_log)


def add_category(request):
    return render(request, 'add_category.html')


def new_category(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            category_name = request.POST['name']
            img = request.FILES['image']
            if category.objects.filter(category_name=category_name).exists():
                messages.info(request, 'Category is already exist')
                return redirect('add_category')

            cat = category.objects.create(
                category_name=category_name, cat_image=img)
            cat.save()

        return redirect(categorys)


def edit_category(request, id):
    if request.user.is_authenticated:
        cat = category.objects.get(id=id)
        return render(request, 'category_update.html', {'cat': cat})

    return redirect(product_details)


def category_update(request, id):
    if request.method == 'POST':
        cat = category.objects.get(id=id)
        category_name = request.POST['name']

        img = request.FILES.get('image', cat.cat_image)

        cat.category_name = category_name
        cat.cat_image = img
        cat.save()

        return redirect(categorys)


def category_delete(request, id):

    dele = category.objects.get(id=id)
    dele.delete()
    return redirect(categorys)


def add_subcategory(request):
    cat = category.objects.all()
    return render(request, 'add_subcategory.html', {'cat': cat})


def new_subcategory(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            cat1 = request.POST.get('name')
            print(cat1)
            try:
                cat = category.objects.get(id=cat1)
            except:
                return redirect(add_subcategory)
            sub_cat = request.POST['sub_name']
            img = request.FILES['image']
            cat = sub_category.objects.create(
                Main_category=cat, name=sub_cat, image=img)
            cat.save()

        return redirect(categorys)


def subcategory_delete(request, id):
    dele = sub_category.objects.get(id=id)
    dele.delete()
    return redirect(categorys)


def edit_subcategory(request, id):
    if request.user.is_authenticated:
        subcat = sub_category.objects.get(id=id)
        cat = category.objects.all()
        return render(request, 'subcategory_edit.html', {'subcat': subcat, 'cat': cat})
    return redirect(product_details)


def subcategory_update(request, id):
    if request.method == 'POST':
        cat = sub_category.objects.get(id=id)
        print(cat)
        cat1 = request.POST.get('name')
        print('name : ', cat1)
        try:
            cat2 = category.objects.get(id=cat1)
        except:
            return redirect(add_subcategory)
        name = request.POST['sub_name']
        img = request.FILES.get('image', cat.image)

        cat.Main_category = cat2
        cat.name = name
        cat.image = img
        cat.save()

        return redirect(categorys)


def user_block(request, id):
    if request.user.is_superuser:
        user = User.objects.get(id=id)
        user.is_active = False
        user.save()
    return redirect(admins_home)


def user_unblock(request, id):
    if request.user.is_superuser:
        user = User.objects.get(id=id)
        user.is_active = True
        user.save()
    return redirect(admins_home)


def order_details(request):
    if request.user.is_superuser:
        order = Order.objects.all()
        return render(request, 'order_details_admins.html', {'orders': order})


def order_delete(request, id):
    if request.user.is_superuser:
        order = Order.objects.get(id=id)
        print(order)
        order.delete()
    return redirect(order_details)


def DashBoard(request):
    if request.user.is_authenticated and request.user.is_superuser:
        cart = Order.objects.all()
        cat = category.objects.all()
        order_count = 0
        revenue = 0

        for i in cart:
            order_count = order_count+1
            revenue = revenue + i.get_final_price()
        product = products.objects.all()
        product_count = 0
        for i in product:
            product_count = product_count+1
        user_list = User.objects.exclude(username='admin')
        user_count = 0
        for i in user_list:
            user_count = user_count+1
        cat_count = []
        for c in cat:
            cat_count.append(products.objects.filter(Category=c.id).count())

        d = Order.objects.filter(method='Cash on delivery').count()
        r = Order.objects.filter(method='Razorpay').count()
        p = Order.objects.filter(method='PayPal').count()
        deliverd_count = Order.objects.filter(status='Delivered').count()
        print('d : ', d)
        return render(request, 'DashBoard.html', {'product': product, 'cart': cart, 'categorys': cat, 'cat_count': cat_count, 'cash': d, 'Razor': r, 'PayPal': p, 'user_count': user_count, 'product_count': product_count, 'order_count': order_count, 'deliverd_count': deliverd_count})
    else:
        return redirect('admin_login')


def StatusUpdate(request, id):
    if request.user.is_superuser:
        if request.method == 'POST':
            newstatus = request.POST['status']
            o = Order.objects.get(id=id)
            o.status = newstatus
            o.save()
            return redirect(order_details)


def SalesReport(request):
    if request.user.is_superuser:
        order = Order.objects.all()
        return render(request, 'SalesReport.html', {'orders': order})
    return redirect(admins_log)


def Offers(request):
    if request.user.is_superuser:
        product_offer = ProductOffer.objects.all()
        category_offer = CategoryOffer.objects.all()
        product = products.objects.all()
        categorys = category.objects.all()
        return render(request, 'Offer.html', {'products': product, 'ProductOffer': product_offer, 'CategoryOffer': category_offer, 'category': categorys})


def AddProductOffer(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            product_id = request.POST['product']
            starting_date = request.POST['starting_date']
            ending_date = request.POST['ending_date']
            offer = request.POST['offer']
            product = products.objects.get(id=product_id)
            new_offer = ProductOffer.objects.create(
                product=product, start_date=starting_date, end_date=ending_date, offer=offer)
            new_offer.save()
            product.p_offer = offer
            product.p_offer_price = math.floor(
                product.price-(product.price*(int(offer)/100)))
            product.save()
            return redirect(Offers)
        return redirect(Offers)
    return redirect(admins_home)


def EditProductOffer(request, id):
    if request.user.is_superuser:
        if request.method == 'POST':
            new_offer = ProductOffer.objects.get(id=id)
            product_id = request.POST['product']
            starting_date = request.POST['starting_date']
            ending_date = request.POST['ending_date']
            offer = request.POST['offer']
            product = products.objects.get(id=product_id)

            new_offer.product = product
            new_offer.offer = offer
            new_offer.start_date = starting_date
            new_offer.end_date = ending_date
            new_offer.save()
            product.p_offer = offer
            product.p_offer_price = math.floor(
                product.price-(product.price*(int(offer)/100)))
            product.save()
            return redirect(Offers)
        return redirect(Offers)
    return redirect(admins_home)


def RmoveProductOffer(request, id):
    offer = ProductOffer.objects.get(id=id)
    p_id = offer.product.id
    product = products.objects.get(id=p_id)
    product.p_offer = 0
    product.p_offer_price = 0
    product.save()
    offer.delete()
    return redirect(Offers)


def AddCategoryOffer(request):
    if request.method == 'POST':
        c_id = request.POST['category']
        start = request.POST['starting_date']
        end = request.POST['ending_date']
        offer = request.POST['offer']
        print(c_id, start, end, offer)

        categorys = category.objects.get(id=c_id)
        new_offer = CategoryOffer.objects.create(
            category=categorys, start_date=start, end_date=end, offer=offer)
        new_offer.save()
        categorys.offer = offer
        categorys.save()
        product = products.objects.filter(Category_id=categorys)
        for i in product:
            i.c_offer = offer
            i.c_offer_price = math.floor(i.price-(i.price*(int(offer)/100)))
            i.save()
        return redirect(Offers)


def EditCategoryOffer(request, id):
    if request.method == 'POST':
        c_id = request.POST['category']
        start = request.POST['starting_date']
        end = request.POST['ending_date']
        offer = request.POST['offer']

        categorys = category.objects.get(id=c_id)
        new_offer = CategoryOffer.objects.get(id=id)
        new_offer.category = categorys
        new_offer.start_date = start
        new_offer.end_date = end
        new_offer.offer = offer
        new_offer.save()

        categorys.offer = offer
        categorys.save()
        product = products.objects.filter(Category_id=categorys)
        for i in product:
            i.c_offer = offer
            i.c_offer_price = math.floor(i.price-(i.price*(int(offer)/100)))
            i.save()
        return redirect(Offers)


def RmoveCategoryOffer(request, id):
    offer = CategoryOffer.objects.get(id=id)
    c_id = offer.category.id
    categorys = products.objects.get(id=c_id)
    categorys.p_offer = 0
    categorys.p_offer_price = 0
    categorys.save()
    offer.delete()
    return redirect(Offers)


def coupon(request):
    if request.user.is_superuser:
        coupons = Coupon.objects.all()
        for c in coupons:
            print(c.start_date)
        return render(request, 'Coupon.html', {'coupons': coupons})


def AddCoupon(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            code = request.POST['code']
            start_date = request.POST['starting_date']
            end_date = request.POST['ending_date']
            minimum_amount = request.POST['minimum_amount']
            discount_amount = request.POST['discount_amount']
            print(code, start_date, end_date, minimum_amount, discount_amount)
            coupons = Coupon.objects.create(
                code=code, start_date=start_date, end_date=end_date, min_amount=minimum_amount, discount_amount=discount_amount)
            coupons.save()
            return redirect(coupon)
        return redirect(coupon)
    return redirect(admins_log)


def couponEdit(request, id):
    if request.method == 'POST':
        code = request.POST['code']
        start_date = request.POST['start']
        end_date = request.POST['end']
        min_amount = request.POST['min']
        dis_amount = request.POST['dis']

        coupons = Coupon.objects.get(id=id)
        coupons.code = code
        coupons.start_date = start_date
        coupons.end_date = end_date
        coupons.min_amount = min_amount
        coupons.discount_amount = dis_amount
        coupons.save()
        return redirect(coupon)


def couponBlock(request, id):
    coupons = Coupon.objects.get(id=id)
    coupons.is_active = False
    coupons.save()
    return redirect(coupon)


def couponUnblock(request, id):
    coupons = Coupon.objects.get(id=id)
    coupons.is_active = True
    coupons.save()
    return redirect(coupon)


def couponRemove(request, id):
    coupons = Coupon.objects.get(id=id)
    coupons.delete()
    return redirect(coupon)


def coupon_calculation(request):
    if request.user.is_authenticated:
        coupon = request.POST['coupon']
        print(coupon)


def sales_date_wise(request):
    start = request.POST['start_date']
    end = request.POST['end_date']
    if len(start) < 1:
        messages.error(request, "choose Date")
        return redirect(SalesReport)
    if len(end) < 1:
        messages.error(request, "choose Date")
        return redirect(SalesReport)

    order = Order.objects.filter(ordered_date__range=[start, end])

    new_order_list = []
    for i in order:
        old = Order.objects.filter(id=i.id, user=i.user)
        for j in old:
            od = {'id': i.id, 'ordered_date': i.ordered_date, 'user': i.user, 'quantity': i.quantity,
                  'get_final_price': j.get_final_price, 'method': i.method, 'status': i.status}
            new_order_list.append(od)
            print('order', new_order_list)
    o_count = len(order)
    return render(request, 'SalesReport.html', {'orders': new_order_list, 'o_count': o_count})


def sales_year_wise(request):
    month = request.POST['month']
    year = request.POST['year']
    print('year : ', year)
    if (year == 'Select'):
        messages.info(request, "Select the year")
        return redirect(SalesReport)
    print(month, year)
    if month == 'all':
        order = Order.objects.filter(ordered_date__year=year)
        new_order_list = []
        for i in order:
            old = Order.objects.filter(id=i.id, user=i.user)
            for j in old:
                od = {'id': i.id, 'ordered_date': i.ordered_date, 'user': i.user, 'quantity': i.quantity,
                      'get_final_price': j.get_final_price, 'method': i.method, 'status': i.status}
                new_order_list.append(od)
        o_count = len(order)
        return render(request, 'SalesReport.html', {'orders': new_order_list, 'o_count': o_count})
    else:
        print("seperate")
        order = Order.objects.filter(
            ordered_date__year=year, ordered_date__month=month)
        new_order_list = []
        for i in order:
            old = Order.objects.filter(id=i.id, user=i.user)
            for j in old:
                od = {'id': i.id, 'ordered_date': i.ordered_date, 'user': i.user, 'quantity': i.quantity,
                      'get_final_price': j.get_final_price, 'method': i.method, 'status': i.status}
                new_order_list.append(od)
        o_count = len(order)
        return render(request, 'SalesReport.html', {'orders': new_order_list, 'o_count': o_count})
