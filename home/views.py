from nis import cat
from django.shortcuts import render,redirect
from admins.models import products,category,Coupon,ProductOffer,CategoryOffer
from members.models import CustomUser
from home.models import Cart,Address,Order,Wishlist
from django.http import JsonResponse,HttpResponse
from django.contrib import messages
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import FileResponse
from django.views.decorators.cache import never_cache
from members.views import user_login
from datetime import datetime,timedelta

# import pagination 
from django.core.paginator import Paginator

# Create your views here.
def home(request):
    product = products.objects.all().order_by('-id')[:12]
    p_offer = ProductOffer.objects.all()
    c_offer = CategoryOffer.objects.all()
    cat = category.objects.all()
    now = datetime.now().date()
    c_active = True
    p_active = True
    for p in p_offer:
        print('date : ',p.end_date)
        if p.end_date < now:
            p.is_active = False
            p_active = False
    for c in c_offer:
        print('date : ',p.end_date)
        if c.end_date < now:
            c.is_active = False
            c_active = False
    # Set up Pagination
    p = Paginator(product,4)
    page = request.GET.get('page')
    venues = p.get_page(page)
    nums = "a" * venues.paginator.num_pages 
    return render(request,'home.html',{'cat':cat,'products':product,'venues':venues,'nums':nums,'now':now,'c_active':c_active,'p_active':p_active})

def shop(request,id):
    cat = category.objects.all()
    cat_id = category.objects.get(id=id)
    prod = cat_id.products_set.all()
    return render(request,'shop.html',{'products':prod,'cat':cat})

def product(request,id):
    cat=category.objects.all()
    product = products.objects.filter(id=id)
    return render(request,'product.html',{'pro':product,'cat':cat})

def cart(request):
    cat = category.objects.all()
    if request.user.is_authenticated:
        user = request.user
    else :
        try:
            user = CustomUser.objects.get(username=request.COOKIES['cart'])
        except:
            user = None
    if Cart.objects.filter(user = user):
        
        orders = Cart.objects.filter(user = user)
        count = orders.count()
        total_amount = 0
        for order in orders:
            total_amount = total_amount + order.get_final_price()
        return render(request,'cart.html',{'orders':orders,'total_amount':total_amount,'count':count,'cat':cat})
    return render(request,'cart.html',{'message':"Your cart is Empty",'cat':cat})

def add_to_cart(request,id):
    product = products.objects.get(id=id)
    if request.user.is_authenticated:
        user = request.user
    else:
        device = request.COOKIES['cart']
        print(device)
        if CustomUser.objects.filter(username = request.COOKIES['cart']):
            user = CustomUser.objects.get(username = request.COOKIES['cart'])
        else:
            user = CustomUser.objects.create_user(username = request.COOKIES['cart'],phone_number = 0)
    if Cart.objects.filter(user=user,product=product):
        item = Cart.objects.get(user=user,product=product)
        item.quantity = item.quantity + 1
        item.save()
        messages.info(request,'Product added to cart')
        return redirect('product',id=id)
    else :
        Cart.objects.create(user=user,product=product)
        messages.info(request,'Product added to cart')
        return redirect('product',id = id)

def add_to_cart_from_shop(request,id,pid):
    product = products.objects.get(id=pid)
    if request.user.is_authenticated:
        user = request.user
    else:
        device = request.COOKIES['cart']
        print(device)
        if CustomUser.objects.filter(username = request.COOKIES['cart']):
            user = CustomUser.objects.get(username = request.COOKIES['cart'])
        else:
            user = CustomUser.objects.create_user(username = request.COOKIES['cart'],phone_number = 0)
    if Cart.objects.filter(user=user,product=product):
        item = Cart.objects.get(user=user,product=product)
        item.quantity = item.quantity + 1
        item.save()
        messages.info(request,'Product added to cart')
        return redirect('shop',id=id)
    else :
        Cart.objects.create(user=user,product=product)
        messages.info(request,'Product added to cart')
        return redirect('shop',id=id)

def add_to_cart_from_home(request,id,pid):
    product = products.objects.get(id=pid)
    if request.user.is_authenticated:
        user = request.user
    else:
        device = request.COOKIES['cart']
        print(device)
        if CustomUser.objects.filter(username = request.COOKIES['cart']):
            user = CustomUser.objects.get(username = request.COOKIES['cart'])
        else:
            user = CustomUser.objects.create_user(username = request.COOKIES['cart'],phone_number = 0)
    if Cart.objects.filter(user=user,product=product):
        item = Cart.objects.get(user=user,product=product)
        item.quantity = item.quantity + 1
        item.save()
        messages.info(request,'Product added to cart')
        return redirect('home')
    else :
        Cart.objects.create(user=user,product=product)
        messages.info(request,'Product added to cart')
        return redirect('home')

def quantity_minus(request,id):
    if request.user.is_authenticated:
        user = request.user
    else:
        user = CustomUser.objects.get(username = request.COOKIES['cart'])
    order_item = Cart.objects.get(id=id)
    qty = order_item.quantity - 1
    Cart.objects.filter(id = id).update(quantity = qty)
    updated_price = Cart.objects.get(id = id).get_final_price()
    orders = Cart.objects.filter(user=user)
    total_amount = 0
    for order in orders:
        total_amount = total_amount + order.get_final_price()
    return JsonResponse({'qty':qty,'total_amount':total_amount,'updated':updated_price})

def quantity_plus(request,id):
    if request.user.is_authenticated:
        user = request.user
    else:
        user = CustomUser.objects.get(username = request.COOKIES['cart'])
    order_item = Cart.objects.get(id=id)
    qty = order_item.quantity + 1
    Cart.objects.filter(id = id).update(quantity = qty)
    updated_price = Cart.objects.get(id = id).get_final_price()
    orders = Cart.objects.filter(user=user)
    total_amount = 0
    for order in orders:
        total_amount = total_amount + order.get_final_price()
    return JsonResponse({'qty':qty,'total_amount':total_amount,'updated':updated_price})

def remove_item(request,id):
    order_item = Cart.objects.get(id=id)
    order_item.delete()
    return redirect(cart)


def profile(request):
    if request.user.is_authenticated:
        cat = category.objects.all()
        user = CustomUser.objects.filter(id=request.user.id)
        address = Address.objects.filter(user=request.user)
        print(address)
        return render(request,'profile.html',{'user':user,'cat':cat,'address':address})
    return redirect(user_login)

def EditProfile(request):
    if request.user.is_authenticated:
        cat = category.objects.all()
        user = CustomUser.objects.filter(id=request.user.id)
        print(user)
        return render(request,'ProfileEdit.html',{'cat':cat,'user':user})
    return redirect(home)

def ProfileUpdate(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user = CustomUser.objects.get(id=request.user.id)
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
            username = request.POST['username']
            email = request.POST['email']
            phonenumber = request.POST['phonenumber']

            user.first_name = firstname
            user.last_name = lastname
            user.username = username
            user.email = email
            user.phone_number = phonenumber
            user.save()
            return redirect(profile)
        return redirect(profile)
    return redirect(home)

def EditPassword(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            OldPassword = request.POST['oldpassword']
            NewPassword1 = request.POST['newpassword1']
            NewPassword2 = request.POST['newpassword2']
            user = request.user
            if NewPassword1 != NewPassword2:
                messages.info(request,"The passwords are not matching")
            elif not user.check_password(OldPassword):
                messages.info(request,"Current password is incorrect")
            else:
                user.password = NewPassword1
                user.save()
                return redirect(profile)
        return redirect(profile)
    return redirect(home)

def addr(request):
    if request.user.is_authenticated:
        return render(request,"address.html")

def  address(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user = CustomUser.objects.get(id=request.user.id)
            print(user)
            name = request.POST['name']
            addr = request.POST['address']
            district = request.POST['district']
            state = request.POST['state']
            pin_code = request.POST['pin_code']
            contact_number = request.POST['contact_number']
            additional_number = request.POST['additional_number']

            address = Address.objects.create(user = user,name = name,address = addr,district = district,state = state,pin_code = pin_code,contact_number = contact_number,additional_number=additional_number)
            address.save()

            return redirect(profile)
        return redirect(profile)

def AddressEdit(request,id):
    if request.user.is_authenticated:
        address = Address.objects.get(id=id)
        return render(request,"AddressEdit.html",{"address":address})
    return redirect(home)

def AddressUpdate(request, id):
    if request.method == 'POST':
        address = Address.objects.get(id=id)
        name = request.POST['name']
        addr = request.POST['address']
        district = request.POST['district']
        state = request.POST['state']
        pin_code = request.POST['pin_code']
        contact_number = request.POST['contact_number']
        additional_number = request.POST['additional_number']

        address.name = name
        address.address = addr
        address.district = district
        address.state = state
        address.pin_code = pin_code
        address.contact_number = contact_number
        address.additional_number = additional_number
        address.save()

        return redirect(profile)

def AddressDelete(request,id):
    if request.user.is_authenticated:
        address = Address.objects.get(id=id)
        address.delete()
    return redirect(home)

@never_cache
def checkout(request):
    if request.user.is_authenticated:
        cat = category.objects.all()
        user = CustomUser.objects.get(id=request.user.id)
        address = Address.objects.filter(user_id = user)
        if Cart.objects.filter(user = request.user):
            orders = Cart.objects.filter(user = request.user)
            total_amount = 0
            for order in orders:
                total_amount = total_amount + order.get_final_price()
            return render(request,'checkout.html',{'orders':orders,'total_amount':total_amount,'cat':cat,'address':address})
    return redirect(user_login)

def coupon_applay(request,code):
    now = datetime.now()
    print(len(code))
    global cod 
    cod = code
    print ('cod = ',cod)
    if len(code) == 0:
        return redirect(checkout)
    else:
        print(code)
        cat = category.objects.all()
        user = CustomUser.objects.get(id=request.user.id)
        address = Address.objects.filter(user_id = user)
        if Cart.objects.filter(user = request.user):
            print('in')
            orders = Cart.objects.filter(user = request.user)
            total_amount = 0
            for order in orders:
                total_amount = total_amount + order.get_final_price()
        try:
            coupon=Coupon.objects.get(code__contains=code)
            print(coupon)
            print('end_date',coupon.end_date)
            print('today',datetime.date.today())
        except:
            return JsonResponse({'errormessage':"Invalid Coupon Code",'total_amount':total_amount,'discount_amount':'0.0'})
        if coupon.is_active:
            if total_amount<coupon.min_amount:
                return JsonResponse({'errormessage':"Offer only applicable for purchases above "  + str(coupon.min_amount),'total_amount':total_amount,'discount_amount':'0.0'})
            elif (now.date() < coupon.start_date and now.date() > coupon.end_date()):
                return JsonResponse({'errormessage': "Coupon Has Expired", 'total_amount':total_amount,'discount_amount':'0.0'})
            else:
                total_amount = total_amount-coupon.discount_amount
                print(total_amount,' ',coupon.discount_amount)
                return JsonResponse({'message':"Coupon has been applied",'total_amount':total_amount,'discount_amount':coupon.discount_amount})
                
        else:
            return JsonResponse({'errormessage':"Coupon Expired " ,'total_amount':total_amount,'discount_amount':'0.0'})


def placeorder(request):
    if request.method == 'POST':
        user = CustomUser.objects.get(id=request.user.id)
        payment = request.POST.get('payment')
        print(payment)
        address_id = request.POST.get('address_id')
        print(address_id)
        addr = Address.objects.get(id = address_id)
        orders = Cart.objects.filter(user = request.user)
        total_amount = 0
        total_amount_offer = 0
        
        try:
            coupon = Coupon.objects.get(code__contains=cod)
        except:
            coupon = None
        if coupon == None or coupon.min_amount < total_amount:
            for order in orders:
                total_amount = total_amount + order.get_final_price()
                orders = Order.objects.create(user = user ,amount = total_amount ,method = payment ,ordered = True,address = addr,product = order.product,quantity = order.quantity)
                orders.save()
                return render(request,'success.html')
        else:
            coupon_per_prod=coupon.discount_amount/orders.count()
            for order in orders:
                total_amount_offer = total_amount_offer + order.get_final_price()
                offer_amount = total_amount_offer - coupon_per_prod
                orders = Order.objects.create(user = user ,amount = total_amount_offer ,method = payment ,ordered = True,address = addr,product = order.product,quantity = order.quantity,coupon_code = cod,discounted_amnt = offer_amount)
                orders.save()
                return render(request,'success.html')
    return redirect(checkout)

def Razorpay(request):
    user = CustomUser.objects.get(id=request.user.id)
    orders = Cart.objects.filter(user = request.user)
    total_amount = 0
    for order in orders:
      total_amount = total_amount + order.get_final_price()
    grand_total = int(total_amount)
    return JsonResponse({'total': grand_total,})

def orders(request):
    if request.user.is_authenticated:
        product_price = 0
        cat = category.objects.all()
        order = Order.objects.filter(user = request.user)
        for o in order:
            price = o.discounted_amnt/o.quantity
            product_price = price
        return render(request,'order_details.html',{'orders':order,'product_price':product_price,'cat':cat})
    return(home)

def orders_delete(request,id):
    if request.user.is_authenticated:
        order=Order.objects.get(id=id)
        print(order)
        order.delete()
    return redirect(orders)

def wishlist(request):
    if request.user.is_authenticated:
        cat = category.objects.all()
        wishlist = Wishlist.objects.filter(user=request.user)
        return render(request,'wishlist.html',{'wishlist':wishlist,'cat':cat})
    return redirect(user_login)

def AddToWishlist(request):
    print("entered")
    if request.method == 'GET':
        user = request.user
        print(user)
        prod_id = request.GET['prod_id']
        print(prod_id)
        product = products.objects.get(id=prod_id)
        wishlist = Wishlist.objects.create(user=user,product=product)
        wishlist.save()
        return JsonResponse({'status': True})

def RemoveFromWish(request,id):
    if request.user.is_authenticated:
        wish = Wishlist.objects.get(id=id)
        wish.delete()
        return redirect(wishlist)

def invoice(request,id):
    if request.user.is_authenticated:
        cart = Order.objects.get(id=id)
        user = request.user
        template_path = 'invoice.html'


        context = {'cart':cart,'user':user}

        response = HttpResponse(content_type='application/pdf')
        response['Content-Didpodition'] = 'filename = "Order invoice.pdf"'
        template = get_template(template_path)
        html = template.render(context)

        pisa_status = pisa.CreatePDF(html,dest=response)
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>'+html+'<pre>')
        return(response)

def returnItem(request,id):
    if request.user.is_authenticated:
        order = Order.objects.get(id=id)
        order.status = "Return"
        order.save()
        print(order.status)
        return redirect(orders)