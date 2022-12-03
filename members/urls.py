from django.urls import path
from . import views 

urlpatterns = [
    path('login',views.user_login,name = "login"),
    path('signup',views.user_signup,name= "signup"),
    path('logout',views.user_logout,name = "logout"),
    path('number_check',views.number_check,name="number_check"),
    path('otp_validate',views.otp_validate,name="otp_validate"),
    path('signup_otp',views.otp_validate_signup,name="signup_otp"),
    path('resendOtp',views.resendOtp,name = 'resendOtp')
]