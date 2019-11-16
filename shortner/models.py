from django.conf import settings
#from django.urls import reverse
from django.db import models
from django.utils.encoding import smart_text
from django_hosts.resolvers import reverse

from .utils import code_generator,create_shortcode
from .validators import validate_url,validate_dot_com
#Custom Login
from django.contrib.auth.models import (
    BaseUserManager,AbstractBaseUser
)

from django.core.validators import RegexValidator


SHORTCODE_MAX = getattr(settings,"SHORTCODE_MAX",15)


# Create your models here.
class TreyeURLManager(models.Manager):
    def all(self,*args,**kwargs):
        qs_main = super(TreyeURLManager,self).all(*args,**kwargs)
        qs = qs_main.filter(active=True)
        return qs

    def refresh_shortcodes(self, items=None):
        qs = TreyeURL.objects.filter(id__gte=1)
        if items is not None and isinstance(items,int):
            qs = qs.order_by('-id')[:items]
        new_codes = 0
        for q in qs:
            q.shortcode = create_shortcode(q)
            print(q.id)
            q.save()
            new_codes += 1
        return "New codes made: {i}".format(i=new_codes)

class TreyeURL(models.Model):
    url       = models.CharField(max_length=220, validators=[validate_url,validate_dot_com])
    shortcode = models.CharField(max_length =SHORTCODE_MAX, unique = True,blank = True)
    updated   = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    active    = models.BooleanField(default = True)

    objects = TreyeURLManager()

    def save(self, *args, **kwargs):
        if self.shortcode is None or self.shortcode == "":
            self.shortcode = create_shortcode(self)
        if not "http" in self.url:
            self.url = "http://" + self.url
        super(TreyeURL, self).save(*args, **kwargs)

    # def my_save(self):
    #     self.save()

    def __str__(self):
        return smart_text(self.url)

    def __unicode__(self):
        return smart_text(self.url)

    def get_short_url(self):
        url_path = reverse("scode",kwargs={'shortcode':self.shortcode},host='www',scheme='http')
        return url_path

class Login_user(models.Model):
    username = models.CharField(max_length=130)
    email = models.EmailField(blank=False)
    password = models.CharField(max_length=30, blank=False)