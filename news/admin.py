from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Post, PostCategory, Author


admin.site.register(Post)
admin.site.register(PostCategory)
admin.site.register(Author)