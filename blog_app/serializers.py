from xmlrpc.client import boolean
from rest_framework import serializers
from .models import (
    Post, Section, Comment, Reply, Image
)
from rest_framework.serializers import ValidationError
from rest_framework.serializers import (
    ValidationError,
    SerializerMethodField,
    HyperlinkedModelSerializer
)


class PostSerializer(serializers.ModelSerializer):
    post_image = serializers.ImageField(required=False, read_only=True)
    
    class Meta:
        model = Post
        fields = "__all__"
        extra_kwargs = {
            "post_image": {
                "validators": []
            }, 
        }
        
    def validate(self, data):
        print("[validate]: inside validate")
        print(data)
        
        # initial data
        # initial_data = self.initial_data
        # print(initial_data)
        
        # save images
        
        
        return data

    def create(self, request):   
        # save validated data
        instance = self.Meta.model(**self.validated_data)
        instance.save()
        
        # initial data
        initial_data = self.initial_data
        
        # save images
        image = request.FILES.getlist("post_image", None)
       
        if len(image) > 0:  
            instance.post_image.create(image_content=image[0])
        
        # add sections
        sections = initial_data.get("post_section")
        
        if len(sections) > 0:
            # author, title, content, public
            author = instance.post_author
            
            for section in sections:
                section_obj = Section(
                    section_post=instance,
                    section_author=author,
                    section_title=section.get("section_title", None),
                    section_content=section.get("section_content", None),
                    section_public=bool(section.get("section_public", None))
                )
                
                section_obj.save()
                 
                images  = section.get("section_image")
                
                print(images)
          
                if len(images) > 0:
                    for image in images:
                        section_obj.section_image.create(
                            image_related_post=instance,
                            image_content=image
                        )
            
        return instance
        
        
class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = "__all__"
        
    def validate(self, data):
        # print("[validate]: inside validate")
        # print(data)
        
        # initial data
        # initial_data = self.initial_data
        # print(initial_data)
        
        # save images
        
        
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
        
        # pass


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
        
        # 
        
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = "__all__"



