from django.db.models.signals import post_save,m2m_changed
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models  import Profile
from posts.models import Following

@receiver(post_save,sender=User)
def create_profile(sender,instance,created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        Following.objects.create(user=instance)

@receiver(post_save,sender=User)
def update_profile(sender,instance ,**kwargs):
    
    instance.profile.save()
# @receiver(m2m_changed,sender = Following.following.through )
# def add_follower(sender,instance,action,reverse,pk_set,**kwargs):
#     followed_user =[]
#     logged_user = User.objects.get(username= instance)
#     for h in pk_set:
#         user =User.objects.get(pk=h)
#         Following_obj =Following.objects.get(user = user)
#         followed_user.append(Following_obj)
    
#     if  action=='pre_add':
#         for i in followed_user:
#             i.follower.add(logged_user)
#             i.follower.save()


#     elif  action=='pre_remove':
#         for k in followed_user:
#             k.follower.remove(logged_user)
#             k.follower.save()