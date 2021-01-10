from django.shortcuts import render,redirect,HttpResponseRedirect,HttpResponse
from itertools import chain
from django.views.generic import ListView,CreateView,DeleteView,UpdateView
from .models import *
from system.models import Profile
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from system.forms import CommentForm
import random
import json
# from .form import PostCreate
# Create your views here. 

class PostCreateView(CreateView,LoginRequiredMixin):
    model=UserPost
    fields=[
        'song',
        'cover',
        'songname'
    ]
    def form_valid(self,form):
        form.instance.artist=self.request.user
        return super().form_valid(form)


class PostUpdateView(UpdateView,LoginRequiredMixin):
    model=UserPost
    fields=[
        'cover' 
    ]

class PostDeleteView(DeleteView,LoginRequiredMixin):
    model=UserPost
    template_name='profile.html'
    success_url='/profile'

@login_required
def systempost(request):
    syspost=Post.objects.all()
    userpost=UserPost.objects.all()
    
    userlist=[]
    syslist=[]
    for l in userpost:
        userlist.append(l)
    random.shuffle(userlist)
    random_five=userlist[0:7]  
    for j in syspost:
        syslist.append(j)
    random.shuffle(syslist)
    random_sys=syslist[0:7]

    heading=Heading.objects.all()

    special=Special.objects.all()
    return render(request,'home.html',locals())

class SearchView(ListView,LoginRequiredMixin):
    template_name='search.html'
    paginate_by=20
    count=0
    def get_context_data(self, *args ,**kwargs):
        context=super().get_context_data(*args,**kwargs)
        context['count'] = self.count or 0
        context['query'] =self.request.GET.get('q')
        return context
    def get_queryset(self):
        request=self.request
        query =request.GET.get('q', None)
    
        if query is not None:
            userpost=UserPost.objects.search(query)
            syspost=Post.objects.search(query)
            user=Profile.objects.search(query)

            queryset_chain=chain(
                userpost,
                syspost,
                user
                
            )
            qs = sorted(queryset_chain, 
                        key=lambda instance: instance.pk, 
                        reverse=True)
            self.count = len(qs) # since qs is actually a list
            return qs
        return Post.objects.none()
@login_required
def song(request,id):
    banner = Special.objects.get(id=id)
    post = Post.objects.filter(special=banner.title)
    return render(request,'song.html',locals())
@login_required   
def details_user(request,id):
    song=UserPost.objects.get(id=id)
    artist=Profile.objects.get(user=song.artist)
    
    userpost=UserPost.objects.all()
    
    userlist=[]
    
    for l in userpost:
        userlist.append(l)
    random.shuffle(userlist)
    random_five=userlist[0:7]  
    
    return render(request,'detail_user.html',locals())

@login_required
def detail(request,id):
    song = Post.objects.get(id=id)
    syspost=Post.objects.all()
    syslist=[] 
    for j in syspost:
        syslist.append(j)
    random.shuffle(syslist)
    random_sys=syslist[0:7]
    # name_list = []
    # for j in random_sys:
    #     if len(j.artist)>15:
    #         name_list.append(str(j.artist)[:15]+"...")
    #     else:
    #         name_list.append(j.artist)
    
    return render(request,'detail.html',locals())


@login_required
def comment_post(request,id):
    post = UserPost.objects.get(id=id)
    comments = Comment.objects.filter(post=post).order_by('-id')
    
    if request.method=='POST':
        c_form = CommentForm(request.POST,instance=post)
        if c_form.is_valid():
            content = request.POST.get('content')
            content1 = str(content)
            for j in content1:
                if j=='\r' or j=='\n':
                    content1=content1.replace(j,' ')
           
            c_form = Comment.objects.create(post=post,name=request.user,content=content1)
            c_form.save()
            return redirect('detail_user',id)
    else:
        c_form = CommentForm(instance=post)


    return render(request,'comments.html',locals())



    


 



