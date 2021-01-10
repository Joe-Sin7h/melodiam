from django.shortcuts import render,redirect,HttpResponse
from posts.models import UserPost,Post,Following
from .forms import CreateUserForm,ProfileUpdateForm,UserUpdateForm,FeedbackForm
from django.contrib import messages
from django.views.generic import ListView,CreateView,DeleteView,FormView
from django.contrib.auth.decorators import login_required
from .filters import Search
from django.contrib.auth.models import User
from itertools import chain
from .models import Profile,Feedback
from posts.models import Special,Post
from django.contrib.auth.mixins import LoginRequiredMixin
import json

from django.contrib.messages.views import  SuccessMessageMixin

# Create your views here.
def melodiam(request):
    return render(request,'melodiam.html')

def register(request):
    form=CreateUserForm(request.POST or None)
    if form.is_valid():
        form.save()
        form=CreateUserForm()
        messages.success(request,'registration successful login now')
        return redirect('login')

    return render(request,'register.html',{'form':form})
@login_required
def editprofile(request):
    u_form=UserUpdateForm(instance=request.user)
    p_form=ProfileUpdateForm(instance=request.user.profile)
    if request.method=='POST':
        u_form=UserUpdateForm(request.POST,instance=request.user)
        p_form=ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile,)
        if u_form.is_valid() and p_form.is_valid():
            p_form.save() 
            u_form.save()
             

    return render(request,'editprofile.html',locals())
   

@login_required
def UserListView(request):
    user=User.objects.get(username=request.user)
    post=UserPost.objects.filter(artist=request.user)
    # following_ = Following.objects.get(user=request.user) 
    total=len(post)
    profile = Profile.objects.get(user=user)
    following_obj = Following.objects.get(user = user)
    follower,following = following_obj.follower.count(), following_obj.following.count()
    
    return render(request,'profile.html',locals())


@login_required    
def settings(request):
    return render(request,'settings.html')  


def about(request):
    return render(request,'about.html')
def contact(request):
    return render(request,'contact.html')

@login_required
def artist(request,username):

    user_=User.objects.get(username=username)
    creator=Profile.objects.get(user=user_)
    post=UserPost.objects.filter(artist=creator.user)
    total = len(post)

    
    if creator.user==request.user :
        return redirect('profile')
    else:
        
        following_obj = Following.objects.get(user = user_)
        follower,following = following_obj.follower.count(), following_obj.following.count()
    
        return render(request,'artist.html',locals())

@login_required
def follow(request,username):
    to_follow=User.objects.get(username=username)
    following =Following.objects.filter(user=request.user,following=to_follow)
    being_followed = Following.objects.filter(user=to_follow)
    is_following = True if following else False
    if is_following:
       
        Following.unfollow(request.user,to_follow)
        for i in being_followed:
            if i.follower==request.user:
                i.follower.remove(request.user)
        is_following=False
    else:
  
        Following.follow(request.user,to_follow)
        for i in being_followed:
            i.follower.add(request.user)
        is_following=True
    
    resp={
        'following':is_following,
        'follow':following
    }
    response=json.dumps(resp)

    return HttpResponse(response,content_type='application/json',)
@login_required
def followinglist(request):
    flist = Following.objects.filter(user=request.user)
    flo = flist[0].following.all()
    ProfileUsers = [Profile.objects.get(user=x) for x in flo]
    
        
    return render(request,'following.html',locals())
@login_required   
def followerlist(request):
    flist = Following.objects.filter(user=request.user)
    flo = flist[0].follower.all()
    ProfileUsers = [Profile.objects.get(user=x) for x in flo]
    return render(request,'follower.html',locals())

def feedback(request):
    c_form=CreateUserForm(request.POST or None,user=request.user)
    if c_form.is_valid():

        form.save()
        form=CreateUserForm()

       
def error_404(request,exception):
    return render(request,"404.html")

@login_required
def albumlist(request,title):
    album = Post.objects.filter(special=title)
    return render(request,'album.html',locals())
