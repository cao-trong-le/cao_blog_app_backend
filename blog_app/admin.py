from django.contrib import admin
from .models import Post, Image, Comment, Reply, Section, File

# Register your models here.
admin.site.register(Post)
admin.site.register(Section)
admin.site.register(Image)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(File)