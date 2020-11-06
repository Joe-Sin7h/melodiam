from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import Q
from PIL import Image


class PostManager(models.Manager):
    def search(self,query=None):
        qs=self.get_queryset()
        if query is not None and query!='':
            or_lookup = (Q(songname__icontains=query))
            qs=qs.filter(or_lookup)
        return qs 
 


# Create your models here.
class UserPost(models.Model):
    artist=models.ForeignKey(User,on_delete=models.CASCADE)
    cover=models.ImageField(upload_to='covers')
    song=models.FileField(upload_to='songs')
    genre=models.CharField(max_length=12 ,default=False)
    date=models.DateField(auto_now_add=True,db_index=True)
    value=models.CharField(max_length=10,default=True,null=False)
    liked=models.ManyToManyField(User,default=None,blank=True,related_name='liked')
    
    songname=models.CharField(max_length=25 , default='',null=False,blank=False)
    objects=PostManager()
    class Meta:
        ordering= ('date',)
    def __str__(self):
        return f'{self.songname}'
    def get_absolute_url(self):
        return reverse('profile')
    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        img=Image.open(self.cover.path)
        if img.height>500 or img.width>500:
            o=(500,500)
            img.thumbnail(o)
            img.save(self.cover.path)
        


class Post(models.Model):
    artist=models.CharField(max_length=50)
    postsong=models.FileField(upload_to='syssong')
    postcover=models.ImageField(upload_to='syscover')
    # description=models.CharField(max_length=80)
    # genre=models.CharField(max_length=12)
    date=models.DateField(auto_now_add=True,null=True)
    special=models.CharField(max_length=20, blank=True , null=True)
    songname=models.CharField(max_length=30,default='',null=False,blank=False)
    value=models.CharField(max_length=10,default=False,null=False)
    objects=PostManager()

    class Meta:
        ordering= ('date',)

    

    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        img=Image.open(self.postcover.path)
        if img.height>500 or img.width>500:
            o=(500,500)
            img.thumbnail(o)
            img.save(self.postcover.path)
    def __str__(self):
        return f'{self.songname} '

class Special(models.Model):
    title =  models.CharField(max_length=100,default=False)
    cover=models.ImageField(upload_to='covers')
    discription=models.CharField(max_length=100,null=True,blank=True)
    head=models.CharField(max_length=50,default=False)



class Heading(models.Model):
    head=models.CharField(max_length=50,default=False)



class Following(models.Model):
    # follower=models.CharField(max_length=100,null=False,default='')
    # following=models.CharField(max_length=100,null=False,default='')
 
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    following = models.ManyToManyField(User,related_name='followed')
    follower = models.ManyToManyField(User,related_name='followers',blank=True)
    @classmethod 
    def follow(cls,user,another):
        obj,create=cls.objects.get_or_create(user=user)
        obj.following.add(another)
    
    @classmethod
    def unfollow(cls,user,another):
        obj , create =cls.objects.get_or_create(user=user)
        obj.following.remove(another)

class Like(models.Model):
    user = models.ManyToManyField(User)
    post = models.OneToOneField(UserPost,on_delete=models.CASCADE)
    # likenumber = models.IntegerField(default=0)

    @classmethod 
    def like(cls,post,user):
        obj,create = cls.objects.get_or_create(post = post)
        obj.user.add(user)

    @classmethod
    def unlike(cls,post,user):
        obj,create = cls.objects.get_or_create(post= post)
        obj.user.remove(user)
    def __str__(self):
        return f"{self.post}"

class Comment(models.Model):
    post = models.ForeignKey(UserPost, on_delete = models.CASCADE)
    name = models.ForeignKey(User,on_delete=models.CASCADE,default=False)
    content = models.TextField(default=None,blank=False)
    postingtime = models.DateTimeField(auto_now_add=True,db_index=True)

    def __str__(self):
        return f'{self.post}'