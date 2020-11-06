from django.contrib import admin
from django.urls import path
from .views import  *
 
urlpatterns=[
   path('home/',systempost,name='systempost'),
   path('song/<int:id>',song,name='song'),
   path('song/detail/<int:id>',detail,name='detail'),
   # path('song/detail/<int:id>/like',detail,name='like'),
   path('song/details/<int:id>',details_user,name='detail_user'),
   path('comments/<int:id>',comment_post,name='detail_comment'),
 

]