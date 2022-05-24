from .serializers import NewUserSerializer, UserSerializer
from blog_app.event_handlers import EventHandler
from .models import NewUser
import jwt
import os

class EventHandler(EventHandler):
    def __init__ (self, request):
        super().__init__(request)
        self.user_event_handler = self.UserEventHandler(request, self.return_value)
        
    class UserEventHandler:
        def __init__(self, request, return_value):
            self.data = request.data
            self.request = request
            self.return_value = return_value
            self.newuser_serializer = NewUserSerializer
            self.user_serializer = UserSerializer
            self.query = NewUser
            
        def login_handler(self):
            self.return_value["event"] = "register"
            
            auth_value = self.request.headers.get("Authorization", None)
            access_token = str(auth_value).split(" ")[1]
            key = os.environ.get("SECRET_KEY")
            payload = jwt.decode(
                jwt=access_token, 
                key=key, 
                algorithms=["HS256"]
            )
            
            print(payload)
            user_id = payload.get("user_id", None)
            if user_id is not None:
                user = self.query.objects.get(id=user_id)
                return_data = self.user_serializer(user).data
                
                self.return_value["data"] = return_data
                self.return_value["message"] = "get user successfully"
                
            return self.return_value
        
        def register_handler(self):
            self.return_value["event"] = "register"
            
            serializer = self.newuser_serializer(data=self.data)
            
            if serializer.is_valid():
                serializer.create(self.request)
                self.return_value["data"] = None
                self.return_value["status"] = True
                self.return_value["message"] = "register user successfully!"
                
            else:
                self.return_value["message"] = "failed !"
                self.return_value["status"] = False
                self.return_value["error"] = serializer.errors
                
            return self.return_value
        
        def get_user_info(self):
            self.return_value["request_event"] = "get_user_infor"
            self.return_value["data"] = self.user_serializer(self.data).data
            self.return_value["message"] = "Get data successfully!"
   
            return self.return_value
            

    
    