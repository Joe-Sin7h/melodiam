from django.contrib import admin
from .models import Post,UserPost,Special,Heading,Following,Like,Comment
admin.site.register(Post)
admin.site.register(UserPost)
admin.site.register(Special)
admin.site.register(Heading)

admin.site.register(Following)
admin.site.register(Like)
admin.site.register(Comment)

# Register your models here.
