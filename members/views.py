from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from .models import CustomUser
from django.contrib.auth import get_user_model
from django.contrib import messages
# from home.views import home
from django.views.decorators.cache import never_cache
from members.mixins import MessageHandler
from members.CustomBackend import *
from home.models import Cart

User = get_user_model() 
# Create your views here.

@never_cache
def user_signup(request):

    if request.method == 'POST':
        global firstname
        global lastname
        global username
        global email
        global phonenumber
        global password1
        global password2

        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        phonenumber = request.POST['phonenumber']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        print(':',phonenumber,':')
        print('length : ',len(phonenumber))
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username is taken')
                return redirect('signup')
            elif User.objects.filter(email = email).exists():
                messages.info(request,'Email is already used')
                return redirect(user_signup)
            elif User.objects.filter(phone_number = phonenumber).exists():
                messages.info(request,'phone number is already used')
                return redirect(user_signup)
            else:
                otp=1
                message_handler = MessageHandler(phonenumber,otp).sent_otp_on_phone()
                return render(request,'signup_otp.html',{'new_phone_number':phonenumber})
        else:
            messages.info(request,'The password is not matching!')
            return redirect('signup')
    else :
        return render(request,'user_signup.html')

@never_cache
def user_login(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password1']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            try:
                guestuser = User.objects.get(username=request.COOKIES['cart'])
            except:
                guestuser = None
            print('GustUser : ',guestuser)
            if guestuser is not None:
                guest_cart = Cart.objects.filter(user = guestuser)
                for item in guest_cart:
                    print(item.user.username,"item.product_idGusest",item.product_id)
                    if Cart.objects.filter(user=user,product=item.product):
                        user_item = Cart.objects.get(user=user, product=item.product)
                        user_item.quantity = user_item.quantity + item.quantity
                        user_item.save()
                        item.delete()
                    else:
                        item.user_id = user.id
                        item.save()
                guestuser.delete()
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request,'invalid credentials')
            return redirect('login')
    else:
        return render(request,'user_login.html')

@never_cache
def user_logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect('/')



otp = 1

def number_check(request):
    if request.method=='POST':
        global phone
        phone=request.POST['phone_number']
        print("phone1=",phone)
        message_handler = MessageHandler(phone,otp).sent_otp_on_phone()
        return redirect('otp_validate')
    return render(request,'otp_phone.html')

def resendOtp(request):
    otp=1
    ph = phonenumber
    print('anas',ph)
    message_handler = MessageHandler(ph,otp).sent_otp_on_phone()
    return redirect(otp_validate_signup)


def otp_validate(request):
    if request.method=='POST':
        otp1= int(request.POST['otp'])
        validate = MessageHandler(phone,otp1).validate()
        print("validate=",validate)
        if validate=="approved":
            user=CustomBackend.authenticate(request,phone_number=phone)
            print("-----")
            print (user)
            return redirect('/')
    return render(request,'otp.html')




def otp_validate_signup(request):
    if request.method == 'POST' and request.POST.get('otp'):
        otp1=request.POST.get('otp')
        print(otp1)
        validate = MessageHandler(phonenumber,otp1).validate()
        print('validate = ',validate)
        if validate == "approved":
            user = User.objects.create_user(first_name=firstname,last_name=lastname,username=username,email=email,password=password1,phone_number=phonenumber)
            user.save()
            auth.login(request,user,backend='django.contrib.auth.backends.ModelBackend')
            return redirect('/')
        
        messages.info("Enter Valid OTP")
    
    # messages.info("Enter valid OTP")
    return render(request,"signup_otp.html")