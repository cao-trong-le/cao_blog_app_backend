from django.shortcuts import render

# Create your views here.
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import NewUserSerializer
from .models import NewUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny

from .event_handler import EventHandler
import json


class NewUserView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = NewUserSerializer
    queryset = NewUser.objects
    
    def get(self, request):
        pass

    def post(self, request, format='json'):
        if request.method == "POST":
            event_handler = EventHandler(request=request)
            
            print(request.data)
            print(request.data.get("event", None))
            
            if request.data.get("event") == "login":
                return_data = event_handler.user_event_handler.login_handler()
                return Response(return_data, status=status.HTTP_200_OK)  
            
            if request.data.get("event") == "register":
                return_data = event_handler.user_event_handler.register_handler()
                print(return_data)
                
                if return_data["status"]:
                    return Response(return_data, status=status.HTTP_201_CREATED) 
                else:
                    return Response(return_data, status=status.HTTP_400_BAD_REQUEST)
             
        return Response({"messsage": "not good"}, status=status.HTTP_400_BAD_REQUEST)


class BlacklistTokenUpdateView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
