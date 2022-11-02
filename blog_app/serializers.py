from symbol import return_stmt
from xmlrpc.client import boolean
from rest_framework import serializers
from .models import (
    Post, Section, Comment, Reply, Image, File
)
from rest_framework.serializers import ValidationError
from rest_framework.serializers import (
    ValidationError,
    SerializerMethodField,
    HyperlinkedModelSerializer
)

from user_management.serializers import UserSerializer
from datetime import datetime
import pytz

from blog_app.helpers.convert import convert_string_bool

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = "__all__"
        
    def validate(self, data):
        return data

    def create(self, validated_data):
        # initial data
        initial_data = self.initial_data
        # print(initial_data)
        
        # save validated data
        instance = self.Meta.model(**validated_data)
        
        # save images
        image = initial_data.get("post_image", None)
        
        if image != "null":
            instance.image_content = image
            
        instance.save()
        
        return instance
    
    def delete_sections(self):
        sections = self.instance
        sections.delete()
        
        return
    
    def update_content(self, data):
        # get section instance
    
        section = self.instance

        section.section_title = data.get("section_title", section.section_title)
        section.section_content = data.get("section_content", section.section_content)
        section.section_public = convert_string_bool(data.get("section_public", section.section_public))
        section.save()
            
        return self.instance
    
    def delete_image(self, data):
        image = self.instance.section_image.get(image_code=data.get("image_code"))
        image.delete()
        
        return self.instance
    
    def add_images(self, request):
        # get a list of new images
        images = request.data.getlist("section_image")
        
        print(images)
        section = self.instance
        
        print(section)
        post = Post.objects.get(post_code=request.data.get("post_code"))
        
        for image in images:
            image_instance = Image(
                image_content=image,
                image_related_post=post,
                image_related_section=section
            )
            
            image_instance.save()
               
        return self.instance
                
    def update_image(self, data):
        section = self.instance
        image = section.section_image.filter(image_code=data.get("image_code", None))
        image.image_content.delete(save=False)
        image.image_content = data.get("new_image", None)
        image.save()
        
        return self.instance

    def get_file_type(self, file):
        file_type = file.name.split(".")[1]
        return file_type
    
    def add_files(self, request):
        section = self.instance
        files = request.data.getlist("section_file", [])
         
        if files:
            for file in files:
                input_data = {
                    "file_related_section": section,
                    "file_content": file,
                    "file_type": self.get_file_type(file)
                }
                
                added_file = File(**input_data)
                added_file.save()
        
        return self.instance
    
class ImageSerializer(serializers.ModelSerializer):
    image_content = serializers.ImageField(required=False, read_only=True)
    
    class Meta:
        model = Image
        fields = "__all__"
        extra_kwargs = {
            "image_content": {
                "validators": []
            }, 
        }
        
    def create(self, validated_data):
        # initial data
        initial_data = self.initial_data
        print(initial_data)
        
        # save validated data
        instance = self.Meta.model(**validated_data)
        
        # save images
        image = initial_data.get("image_content", None)
        if image != "null":
            instance.image_content = image
        instance.save()
        return instance
    
    def update(self):
        # initial data
        initial_data = self.initial_data
        
    def update_section_image(self, new_image):
        image = self.instance 
        image.image_content.delete(save=False)
        image.image_content = new_image
        image.save()
        
        return image
    
    def delete_section_image(self):
        self.instance.delete()
        
        return 
    
class FileSerializer(serializers.ModelSerializer):
    file_content = serializers.FileField(required=False, read_only=True)
    
    class Meta:
        model = File
        fields = "__all__"
        extra_kwargs = {
            "file_content": {
                "validators": []
            }, 
        }
            
    def update_section_file(self, new_file):
        file = self.instance 
        file.file_content.delete(save=False)
        file.file_content = new_file
        file.save()
        
        return file
    
    def delete_section_file(self):
        self.instance.delete()
        
        return 
            
class SectionDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = "__all__"
        depth = 1
        
    image_serializer = ImageSerializer
    file_serializer = FileSerializer
        
    def to_representation(self, instance):
        return_data = super().to_representation(instance)
        
        # get a list of serialized images
        section_images = instance.section_image
        serialized_section_images = self.image_serializer(section_images, many=True).data
        
        return_data["section_image"] = serialized_section_images
        
        # get a list of serialized files
        section_files = instance.section_file
        serialized_section_files = self.file_serializer(section_files, many=True).data
        return_data["section_file"] = serialized_section_files
        
          
        # serialized_section = self.section_serializer(section).data
        # section_images = section.section_image
        # serialized_section_images = self.image_serializer(section_images, many=True).data
        # serialized_section["section_image"] = serialized_section_images
        
        return return_data

class PostDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"
        depth = 1

    image_serializer = ImageSerializer
    section_serializer = SectionSerializer
    section_data_serializer = SectionDataSerializer
        
    def to_representation(self, instance):
        returned_data = super().to_representation(instance)
          
        # retrieve post image
        post_images = instance.post_image.all()
         
        # add post image
        returned_data["post_image"] = None
        if (len(post_images) > 0):
            returned_data["post_image"] = self.image_serializer(post_images[0]).data
            
        returned_data["post_section"] = []
        
        # retrieve all post's sections
        post_sections = instance.section_post.all()
        
        # retrieve section images
        for section in post_sections:
            # serialize section 
            # serialized_section = self.section_serializer(section).data
            # section_images = section.section_image
            # serialized_section_images = self.image_serializer(section_images, many=True).data
            # serialized_section["section_image"] = serialized_section_images
            
            serialized_section = self.section_data_serializer(section).data
            returned_data["post_section"].append(serialized_section)
            
        fields = ["password", "email", "is_staff", "start_date", "is_superuser"]
        
        for field in fields:
            del returned_data["post_author"][field]
        
        return returned_data

class PostSerializer(serializers.ModelSerializer):
    post_image = serializers.ImageField(required=False, read_only=True)
    
    class Meta:
        model = Post
        fields = "__all__"
            
    def validate(self, data):
        return data
    
    def update(self, request):
        # update post

        # replace data if any
        # no need to modify date when update something 
        try:
            self.instance.post_summary = request.data.get("post_summary", self.instance.post_summary)
            self.instance.post_title = request.data.get("post_title", self.instance.post_title)
            self.instance.post_public = convert_string_bool(request.data.get("post_public", str(self.instance.post_public).lower()))
            
            # save the instance
            self.instance.save()
            
        except ValueError as error: 
            raise error
        
        return self.instance
       
    # create function takes in valid data and raw data
    def create(self, original_post, original_sections): 
        # add post
        instance = self.Meta.model(**self.validated_data)
        instance.save()
        
        # save images
        post_images = original_post.get("post_image", None)
       
        if len(post_images) > 0:  
            instance.post_image.create(image_content=post_images[0])
        
        # add sections
        if len(original_sections) > 0:
            # author, title, content, public
            author = instance.post_author
            
            for section in original_sections:
                section_obj = Section(
                    section_post=instance,
                    section_author=author,
                    section_title=section.get("section_title", None),
                    section_content=section.get("section_content", None),
                    section_public=section.get("section_public")
                )
                
                section_obj.save()
                 
                section_images  = section.get("section_image")
                        
                if len(section_images) > 0:
                    for image in section_images:
                        section_obj.section_image.create(
                            image_related_post=instance,
                            image_content=image
                        )
            
        return instance
    
    def save_new_post(self):
        post = self.instance
        post.post_finished = True
        post.save()
        
        return post
               
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"

class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = "__all__"



