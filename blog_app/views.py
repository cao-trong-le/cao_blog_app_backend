from django.shortcuts import render
from rest_framework import generics, status, permissions, viewsets
from django.http import HttpResponse

from .serializers import (
    PostSerializer,
    CommentSerializer,
    ReplySerializer,
    SectionSerializer
)

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
class PostView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = PostSerializer
    queryset = Post.objects
    return_data = None
    
    def get(self, request, key):
        event_handler = None
        
        if request.method == 'GET':
            if (key == "all"):
                self.return_data = event_handler.base_event_handler.get_all_bases()
            else:
                self.return_data = event_handler.base_event_handler.get_bases(key)
            
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
        
        print(request.FILES.get("post_image"))
        
        if request.method == "POST":
            event = request.data.get("event", None)
            
            if event == "add_post":
                return_data = event_handler.post_event_handler.add_post()
                return Response(return_data, status=status.HTTP_201_CREATED)
            
            if event == "delete_post":
                return_data = event_handler.post_event_handler.delete_post()
                return Response(return_data, status=status.HTTP_204_NO_CONTENT)
            
            if event == "delete_posts":
                return_data = event_handler.base_event_handler.delete_bases()
                return Response(return_data, status=status.HTTP_204_NO_CONTENT)
            
            if event == "delete_all_posts":
                return_data = event_handler.base_event_handler.delete_all_bases()
                return Response(return_data, status=status.HTTP_204_NO_CONTENT)
            
            if event == "edit_post":
                return_data = event_handler.base_event_handler.edit_base()
                return Response(return_data, status=status.HTTP_200_OK)
            
            
            # product
            
            # delete a list of obj

            # else:
            #     return Response({"data": "None"}, status=status.HTTP_200_OK)
            
        return Response({'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)