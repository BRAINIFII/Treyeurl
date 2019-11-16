from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.shortcuts import render,get_object_or_404
from django.views import View
from .models import TreyeURL,Login_user
from analytics.models import ClickEvent
from .forms import SubmitUrlForms
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
# Create your views here.

# def signup(self,request,*args,**kwargs):
#     return render(request,"signup.html")

def home_view_fbv(self,request,*args,**kwargs):
    if request.method == 'POST':
        print(request.POST)
    return render(request,"shortner/home.html",{})
    
class HomeView(View):
    def get(self,request,*args,**kwargs):
        the_form = SubmitUrlForms()
        context = {
            "title":"Submit URL",
            "form": the_form
        }
        return render(request,"shortner/home.html",context)
    
    def post(self,request,*args,**kwargs):
        form = SubmitUrlForms(request.POST)
        context = {
                "title":"Submit URL",
                "form": form
        }
        template = "shortner/home.html"
        if form.is_valid():
            new_url = form.cleaned_data.get("url")
            obj, created = TreyeURL.objects.get_or_create(url=new_url)

            context = {
                "object": obj,
                "created": created,
            }
            if created:
                template = "shortner/success.html"
            else:
                template = "shortner/already-exist.html"
        return render(request,template,context)

class URLRedirectView(View):
    def get(self,request,shortcode=None,*args,**kwargs):
        qs = TreyeURL.objects.filter(shortcode__iexact=shortcode)
        if qs.count() != 1 and not qs.exists():
            raise Http404
        obj = qs.first()
        print(ClickEvent.objects.create_event(obj))
        return HttpResponseRedirect(obj.url)
        print(obj.url)

class signup(View):
    def get(self,request,*args,**kwargs):
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('login.html')
            else:
                form = UserCreationForm()
        return render(request,"signup.html",{})

class login(View):
    def get(self,request,*args,**kwargs):
        return render(request,"login.html",{})

class price(View):
    def get(self,request,*args,**kwargs):
        return render(request,"pricing.html",{})

class contact(View):
    def get(self,request,*args,**kwargs):
        return render(request,"contact.html",{})

class about(View):
    def get(self,request,*args,**kwargs):
        return render(request,"about.html",{})

class test(View):
    def get(self,request,*args,**kwargs):
        return render(request,"test.html",{})

class forgotpswd(View):
    def get(self,request,*args,**kwargs):
        return render(request,"forgotpswd.html",{})

class UserCreateView(CreateView):
    model = Login_user
    fields = ('username','email','password')