from django.db import models

# Create your models here.
from shortner.models import TreyeURL

class ClickEventManager(models.Manager):
    def create_event(self,instance):
        if isinstance(instance,TreyeURL):
            obj,created = self.get_or_create(treye_url=instance)
            obj.count+=1
            obj.save()
            return obj.count
        return None

class ClickEvent(models.Model):
    treye_url = models.OneToOneField(TreyeURL,on_delete=models.CASCADE)
    count     = models.IntegerField(default=0)
    updated   = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ClickEventManager()

    def __str__(self):
        return "{i}".format(i=self.count)