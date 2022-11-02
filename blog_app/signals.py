from .models import Post, Section, Image, File
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, post_delete, pre_delete
from django.forms.models import model_to_dict
import json

import boto3

client = boto3.client('s3')

@receiver(pre_delete, sender=Image)
def remove_file_from_s3_post(sender, instance, using, **kwargs):
    instance.image_content.delete(save=False)
    
@receiver(pre_delete, sender=File)
def remove_file_from_s3_post(sender, instance, using, **kwargs):
    instance.file_content.delete(save=False)
    
@receiver(pre_delete, sender=Section)
def remove_file_from_s3_section(sender, instance, using, **kwargs):
    instance.section_image.all().delete()