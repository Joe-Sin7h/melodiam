from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from posts.views import PostCreateView,PostDeleteView,PostUpdateView,SearchView
from .views import *
from .forms import *
urlpatterns = [ 
    path('',melodiam,name='melodiam'),
    path('register/',register,name='register'),
    path('login/',auth_views.LoginView.as_view(template_name='login.html',authentication_form=login),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='melodiam.html'),name='logout'),
    path('profile/',UserListView,name='profile'),
    path('profile/edit/',editprofile,name='editprofile'),
    path('profile/settings/',settings,name='settings'),
    path('profile/create/',PostCreateView.as_view(template_name='createpost.html'),name='create'),
    path('profile/<int:pk>/update',PostUpdateView.as_view(template_name='update.html'),name='update'),
    path('profile/<int:pk>/delete',PostDeleteView.as_view(template_name='delete.html'),name='delete'),
    path('search/',SearchView.as_view(),name='search'),
    path('about/',about,name='about'),
    path('artist/follow/<str:username>/',follow,name='follow'), 
    path('contact/',contact,name='contact'),
    path('artist/<str:username>/',artist,name='artist'),
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='password-reset.html'),name='password_reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),name='password_reset_complete'),
    path('password-change/',auth_views.PasswordChangeView.as_view(template_name='password_change.html'),name='password_change'),
    path('password-change/done',auth_views.PasswordChangeDoneView.as_view(template_name='change_done.html'),name='password_change_done'),
    path('profile/followings',followinglist,name='followinglist'),
    path('porfile/followers',followerlist,name='followerlist'),
    path('album/<str:title>',albumlist,name='albumlist'),
    # path('feedback/',FeedbackView.as_view(),name='fb')
    path("error",error_404)
] 

# handler404 = "system.views.error_404"
