from __future__ import annotations
from django.db import models
# Create your models here.

from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from base.storages import PublicMediaStorage, PrivateMediaStorage
# import blog_app.helpers.generate_code as _generate_code

# from pkg_resources import require
import random
import string
import functools


# Create your models here.

# plan: resize and upload image to aws storage

# User = settings.AUTH_USER_MODEL
User = get_user_model()


def default_image():
    return f"default_image/default.png"

def get_image_filepath(instance, filename):
    obj_class_name = instance.__class__.__name__
    valid_class_names = ["Image"]
    _index = valid_class_names.index(obj_class_name)
    _lowered_class_name = valid_class_names[_index].lower()
    
    # instance fields
    keys = instance.__dict__.keys()
    code = None
    
    for key in keys:
        if "code" in key:
            code = getattr(instance, key)
            break
    
    return f"{_lowered_class_name}_images/{code}/{filename}"

def generate__code(limit, prefix, model, field):
    characters = string.ascii_letters + string.digits + string.punctuation
    flag_check = True
    _code = None
    display_code = None
    _code_list = model.objects.values_list(field, flat=True)
    
    while flag_check:
        _code = "".join(random.choices(list(characters), k=limit))
        display_code = f"#{prefix}{_code}"
        
        if display_code not in _code_list:
            flag_check = False
             
    return display_code

def _post_code():
    return functools.partial(
        generate__code, 
        limit=10, 
        prefix="POST", 
        model=Post,
        field="post_code"
    )()

def _image_code():
    return functools.partial(
        generate__code, 
        limit=10, 
        prefix="IMAGE", 
        model=Image,
        field="image_code"
    )()

def _comment_code():
    return functools.partial(
        generate__code, 
        limit=10, 
        prefix="COMMENT", 
        model=Comment,
        field="comment_code"
    )()

generate__post_code = _post_code
generate__comment_code = _comment_code
generate__image_code = _image_code

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    post_code = models.CharField(
        verbose_name="Post Code", 
        max_length=15, 
        null=False, 
        unique=True, 
        default=generate__post_code
    )
    post_author = models.ForeignKey(
        to=User, 
        related_name="post_user",
        on_delete=models.CASCADE
    )
    post_title = models.CharField(
        verbose_name="Post Title", 
        max_length=255, 
        null=False, 
        unique=True
    )
    post_summary = models.TextField(
        verbose_name="Post Summary", 
        max_length=500, 
        null=True, 
        default=""
    )
    post_public = models.BooleanField(
        verbose_name="Post Public", 
        default=True
    )
    post_likes = models.IntegerField(
        verbose_name="Post Likes",
        default=0
    )
    post_views = models.IntegerField(
        verbose_name="Post Views",
        default=0
    )
    post_edited = models.BooleanField(
        verbose_name="Post Editted",
        default=False
    )
    post_date = models.DateTimeField(
        verbose_name="Post Date",
        auto_now_add=True,
    )
    
    def __str__(self):
        return self.post_title
    
    
class Section(models.Model):
    id = models.AutoField(primary_key=True)
    section_code = models.CharField(
        verbose_name="Section Code", 
        max_length=15, 
        null=False, 
        unique=True, 
        default=generate__post_code
    )
    section_author = models.ForeignKey(
        to=User, 
        related_name="section_user",
        on_delete=models.CASCADE
    )
    section_post = models.ForeignKey(
        to=Post, 
        related_name="section_post",
        on_delete=models.CASCADE
    )
    section_title = models.CharField(
        verbose_name="Section Title", 
        max_length=255, 
        null=True, 
        unique=False,
        default=""
    )
    section_content = models.TextField(
        verbose_name="Section Content", 
        max_length=10000, 
        null=True, 
        default=""
    )
    section_public = models.BooleanField(
        verbose_name="Section Public", 
        default=True
    )
   
    def __str__(self):
        return self.section_title
    
    
class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    comment_code = models.CharField(
        verbose_name="Comment Code", 
        max_length=15, 
        null=False, 
        unique=True, 
        default=generate__comment_code
    )
    comment_content = models.TextField(
        verbose_name="Comment Content", 
        max_length=5000, 
        null=True, 
        default=""
    )
    comment_author = models.ForeignKey(
        to=User, 
        related_name="comment_user",
        on_delete=models.CASCADE
    )
    comment_post = models.ForeignKey(
        to=Post, 
        related_name="comment_post",
        on_delete=models.CASCADE
    )
    comment_time = models.DateTimeField(
        verbose_name="Comment Time",
        auto_now_add=True
    )
    
    def __str__(self):
        return self.comment_code + self.comment_author.username
    
    
class Reply(models.Model):
    id = models.AutoField(primary_key=True)
    reply_code = models.CharField(
        verbose_name="Reply Code", 
        max_length=15, 
        null=False, 
        unique=True, 
        default=generate__comment_code
    )
    reply_content = models.TextField(
        verbose_name="Reply Content", 
        max_length=5000, 
        null=True, 
        default=""
    )
    reply_comment = models.ForeignKey(
        to=Comment, 
        related_name="reply_comment",
        on_delete=models.CASCADE
    )
    reply_author = models.ForeignKey(
        to=User, 
        related_name="reply_user",
        on_delete=models.CASCADE
    )
    reply_post = models.ForeignKey(
        to=Post, 
        related_name="reply_post",
        on_delete=models.CASCADE
    )
    reply_time = models.DateTimeField(
        verbose_name="reply Time",
        auto_now_add=True
    )
    
    def __str__(self):
        return self.reply_code + self.reply_author.username
    
    
class Image(models.Model):
    id = models.AutoField(primary_key=True)
    image_code = models.CharField(
        verbose_name="Image Code", 
        max_length=30, 
        null=False, 
        unique=True, 
        default=generate__image_code
    )
    image_content = models.FileField(
        verbose_name="Image Content", 
        upload_to=get_image_filepath, 
        null=True, 
        default=default_image,
        storage=PublicMediaStorage()
    )
    image_related_post = models.ForeignKey(
        to=Post, 
        related_name="post_image",
        on_delete=models.CASCADE
    )
    image_related_section = models.ForeignKey(
        to=Section, 
        blank=True,
        null=True,
        related_name="section_image",
        on_delete=models.CASCADE
    )
    
    def __str__(self):
        return self.image_code




