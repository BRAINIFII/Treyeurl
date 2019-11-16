from django.contrib import admin
from django.urls import path,include

from shortner.views import HomeView,URLRedirectView,signup,price,contact,test,about,login,forgotpswd

urlpatterns = [
    path('new-admin/', admin.site.urls),
    path('',HomeView.as_view()),
    path('<str:shortcode>', URLRedirectView.as_view(),name='scode'),
    path('Signup/',signup.as_view(),name='signup'),
    path('Login/',login.as_view(),name='login'),
    path('Pricing/',price.as_view(),name='price'),
    path('Contact/',contact.as_view(),name='contact'),
    path('About/',about.as_view(),name='about'),
    path('test-t/',test.as_view(),name='test'),
    path('ForgotPassword/',forgotpswd.as_view(),name='forgotpswd')
]
