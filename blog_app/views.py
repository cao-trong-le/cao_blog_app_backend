from django.shortcuts import render
from rest_framework import generics, status, permissions, viewsets
from django.http import HttpResponse

from .serializers import (
    PostSerializer,
    CommentSerializer,
    ReplySerializer,
    SectionSerializer
)

from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import (
    Post, Section, Image, Comment, Reply
)
import datetime
import json

from django.contrib.auth.models import User

from .event_handlers import EventHandler

# Create your views here.

class SectionView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = SectionSerializer
    queryset = Section.objects
    return_data = None
    
    def post(self, request):
        event_handler = EventHandler(request)
        return_data = None
        
        if request.method == "POST":
            event = request.data.get("event", None)
            
            if event == "create_new_section":
                return_data = event_handler.section_event_handler.add_section()
            
            if event == "update_section_content":
                return_data = event_handler.section_event_handler.update_section()
            
            if event == "delete_sections":
                return_data = event_handler.section_event_handler.delete_sections()
                
            if event == "delete_all_sections":
                return_data = event_handler.section_event_handler.delete_all_sections()
            
            if event == "add_section_images":
                return_data = event_handler.section_event_handler.add_section_images()
                
            if event == "delete_section_image":      
                return_data = event_handler.section_event_handler.remove_section_image()
                
            if event == "update_section_image":
                return_data = event_handler.section_event_handler.update_section_image()
                
            if event == "add_section_files":
                return_data = event_handler.section_event_handler.add_section_files()
                
            if event == "delete_section_file":      
                return_data = event_handler.section_event_handler.remove_section_file()
                
            if event == "update_section_file":
                return_data = event_handler.section_event_handler.update_section_file()
                
                
                
            return Response(return_data, status=return_data["status"])
        
        return Response({'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)

class PostView(APIView):
    # parser_classes = (FileUploadParser,)
    permission_classes = (permissions.AllowAny,)
    serializer_class = PostSerializer
    queryset = Post.objects
    return_data = None
    
    def get(self, request, key):
        event_handler = EventHandler(request)
        
        if request.method == 'GET':
            # print(request.GET.get("key", None), key, user_code)
            if (key == "all"):
                self.return_data = event_handler.post_event_handler.get_all()
            else:
                self.return_data = event_handler.post_event_handler.get_related()
            
                # data = self.serializer_class(bases, many=True).data
            return Response({"data": self.return_data}, status=status.HTTP_200_OK)

            # else:
            #     return Response({"data": "None"}, status=status.HTTP_200_OK)
            
        elif request.method == 'POST':
            print(request.data)
            return Response({"data": "it passes through"}, status=status.HTTP_200_OK)

        return Response({'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request):
        event_handler = EventHandler(request)
        
        if request.method == "POST":
            event = request.data.get("event", None)
            return_data = None
            
            if event == "filter_posts_by":
                return_data = event_handler.post_event_handler.filter_posts()
            
            if event == "get_user_posts":
                return_data = event_handler.post_event_handler.get_user_posts()
            
            if event == "get_all_posts":
                return_data = event_handler.post_event_handler.get_all_posts()
                 
            if event == "add_post":
                return_data = event_handler.post_event_handler.add_post()
                       
            if event == "delete_many_posts":
                return_data = event_handler.post_event_handler.delete_many_posts()
            
            if event == "delete_all_posts":
                return_data = event_handler.post_event_handler.delete_all_posts()
            
            if event == "edit_post":
                return_data = event_handler.post_event_handler.edit_post()
                
            if event == "create_new_post":
                return_data = event_handler.post_event_handler.create_post()
            
            if event == "update_post_heading":
                return_data = event_handler.post_event_handler.update_post_heading()
                print(return_data)
        
            if event == "add_post_heading_image":
                return_data = event_handler.post_event_handler.add_post_heading_image()
     
            if event == "delete_post_heading_image":
                return_data = event_handler.post_event_handler.delete_post_heading_image()
            
            if event == "update_post_heading_image":
                return_data = event_handler.post_event_handler.update_post_heading_image()
                
            if event == "save_new_post":
                return_data = event_handler.post_event_handler.save_new_post()
            
            return Response(return_data, status=return_data["status"])
            
        return Response({'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)