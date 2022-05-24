from .serializers import (
    PostSerializer, 
    SectionSerializer, 
    CommentSerializer, 
    ReplySerializer
)
from .models import Post, Section, Comment, Reply
from django.contrib.auth import get_user_model

User = get_user_model()

class EventHandler:
    def __init__ (self, request):
        self.data = request.data
        self.request = request
        self.return_value = {
            "event": None,
            "data": None,
            "message": None,
            "error": None
        }
        # self.base_event_handler = self.BaseEventHandler(request, self.return_value)
        self.post_event_handler = self.PostEventHandler(request, self.return_value)
    
    
    class PostEventHandler:   
        def __init__(self, request, return_value):
            self.query = Post.objects
            self.data = request.data
            self.request = request
            self.return_value = return_value
            self.base_serializer = PostSerializer
            
        def add_post (self):
            # set request_event
            self.return_value["event"] = self.request.data.get("event", None)
            
            # add author id to data set
            self.data["post_author"] = self.data.get("id", None)
            
            # store data
            serializer = self.base_serializer(data=self.data)
            
            print(serializer.is_valid())
            
            if serializer.is_valid():
                serializer.create(self.request)
                self.return_value["data"] = serializer.data
                self.return_value["message"] = "Data went through."
            else:
                print(serializer.errors)
                
        
            return self.return_value

    class SectionEventHandler:   
        def __init__(self, request, return_value):
            self.query = Section.objects
            self.data = request.data
            self.request = request
            self.return_value = return_value
            self.base_serializer = SectionSerializer
        
        def add_section(self):
            # set request_event
            self.return_value["event"] = self.request.data.get("event", None)
            
            # print({**self.data}.get("base_price"))
            # print(self.data.get("base_group"))
            print(self.data)
            
            # store data
            serializer = self.base_serializer(data=self.data)
            print(serializer.is_valid())
            if serializer.is_valid():
                serializer.save()
                self.return_value["data"] = serializer.data
                self.return_value["message"] = "Data went through."
            else:
                print(serializer.errors)
                
        
            return self.return_value
            
        
        def delete_section(self):
            section_code = self.request.data.get("section_code", None)
            item = self.query.filter(base_code=section_code)
            self.return_value["event"] = self.request.data.get("event", None)
            if item.exists():
                item.delete()
                self.return_value["message"] = "The item has been deleted."
            else:
                self.return_value["message"] = "The item does not exist."
                self.return_value["error"] = "Not Found"
            return self.return_value
      
        def delete_sections(self):
            self.return_value["request_event"] = self.request.data.get("event", None)
            item_codes = self.request.data.get("item_codes", None)
            items = self.query.filter(base_code__in=item_codes)
            if items.exists():
                items.delete()
                self.return_value["message"] = "The items have been deleted."
            else: 
                self.return_value["message"] = "The items do not exist."
                self.return_value["error"] = "Not Found"
            return self.return_value
        
        def delete_all_sections(self):
            self.return_value["request_event"] = self.request.data.get("event", None)
            item_codes = self.request.data.get("item_codes", None)
            items = self.query.all()
            if items.exists():
                items.delete()
                self.return_value["message"] = "The items have been deleted."
            else: 
                self.return_value["message"] = "The items do not exist."
                self.return_value["error"] = "Not Found"
            return self.return_value
       
        
        def edit_section(self):
            # set request_event
            self.return_value["event"] = self.request.data.get("event", None)
            
            # store data
            serializer = self.base_serializer(data=self.data)
            print(serializer.is_valid())
            if serializer.is_valid():
                serializer.update()
                self.return_value["data"] = serializer.data
                self.return_value["message"] = "Data went through."
            else:
                self.return_value["message"] = "The items do not exist."
                self.return_value["error"] = "Not Found"
                
            return self.return_value
            
        
        def get_sections(self, key):
            # set request_event
            self.return_value["request_event"] = self.request.data.get("event", None)
            # filtered_data = self.query.filter()
            self.return_value["data"] = self.base_serializer(self.query.all(), many=True).data 
            self.return_value["message"] = "Collected all bases"
            
            return self.return_value

        
        def get_all_sections(self):
            # set request_event
            self.return_value["request_event"] = self.request.data.get("event", None)
            self.return_value["data"] = self.base_serializer(self.query.all(), many=True).data 
            self.return_value["message"] = "Collected all bases"
            
            return self.return_value
        
        
        
   
    
    