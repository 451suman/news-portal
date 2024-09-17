from django.contrib import admin
from newspaper.models import Contact, Post,Category,Tag,UserProfile, Comment

# Register your models here.
# admin.site.register(Post)
# admin.site.register(Category)
# admin.site.register(Tag)
admin.site.register([Post, Category, Tag, Contact,UserProfile, Comment])

