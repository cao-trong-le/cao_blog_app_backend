from django.db import models
import string
import random
import functools

# Create your models here.
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from base.storages import PrivateMediaStorage, PublicMediaStorage

def default_image():
    return f"default_image/default.png"

def get_image_filepath(instance, filename):
    # get instance class name 
    obj_class_name = instance.__class__.__name__
    valid_class_names = ["NewUser"]
    _index = valid_class_names.index(obj_class_name)
    _lowered_class_name = valid_class_names[_index].lower()
    
    # get username
    username = instance.username
    
    return f"{_lowered_class_name}_images/{username}/{filename}"

class CustomAccountManager(BaseUserManager):
    def create_superuser(self, email, username, first_name, last_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, username, first_name, last_name, password, **other_fields)

    def create_user(self, email, username, first_name, last_name, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(
            email=email, 
            username=username,
            first_name=first_name, 
            last_name=last_name,
            **other_fields)
        user.set_password(password)
        user.save()
        return user
    
def generate__code(limit, prefix, model, field):
    characters = string.ascii_letters + string.digits + string.punctuation
    _code = "".join(random.choices(list(characters), k=limit))
    display_code = f"#{prefix}{_code}"
          
    return display_code

def _user_code():
    return functools.partial(
        generate__code, 
        limit=10, 
        prefix="", 
        model=NewUser,
        field="code"
    )()

generate__user_code = _user_code

class NewUser(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    code = models.CharField(
        verbose_name="User Code", 
        max_length=255, 
        null=True, 
        unique=True, 
        default=generate__user_code
    )
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    about = models.TextField(_(
        'about'), max_length=500, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    avatar = models.FileField(
        verbose_name="User Avatar", 
        upload_to=get_image_filepath,
        null=True, 
        default=default_image,
        storage=PublicMediaStorage()
    )
    objects = CustomAccountManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def __str__(self):
        return self.username