from django.contrib import admin
from newspaper.models import Contact, Post,Category,Tag,UserProfile, Comment, NewsLetter
from django_summernote.admin import SummernoteModelAdmin


# Register your models here.
# admin.site.register(Post)
# admin.site.register(Category)
# admin.site.register(Tag)
admin.site.register([Category, Tag, Contact,UserProfile, Comment, NewsLetter])



class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)

admin.site.register(Post, PostAdmin)