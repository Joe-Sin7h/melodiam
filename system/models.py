from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.db.models import Q
# Create your models here. 
 

class PostManager(models.Manager):
    def search(self,query=None):
        qs=self.get_queryset()
        if query is not None and query!='':
            or_lookup = (Q(name__icontains=query)|Q(user__username__icontains=query))
            qs=qs.filter(or_lookup)
        return qs 


class Profile(models.Model):
    profilepic=models.ImageField(default='user.png',upload_to='images')
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    bio=models.CharField(max_length=35,default=' ',null=True,blank=False)
    name=models.CharField(max_length=22 , default='',null=False,blank=False)
    follower = models.IntegerField(default=0)
    following = models.IntegerField(default=0)
    objects=PostManager()

    def __str__(self):
        return f'{self.user.username}'
    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        img=Image.open(self.profilepic.path)
        if img.height>100 or img.width>100:
            o=(100,100)
            img.thumbnail(o)
            img.save(self.profilepic.path) 

class Feedback(models.Model):
    user = models.CharField(max_length = 100,default=None,blank=False)
    content = models.TextField(blank=False)