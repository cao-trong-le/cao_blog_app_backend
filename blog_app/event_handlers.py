from .serializers import (
    PostSerializer, 
    SectionSerializer, 
    CommentSerializer, 
    ReplySerializer
)
from .models import Post, Section, Comment, Reply
from django.contrib.auth import get_user_model

from django.core.paginator import Paginator

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
            self.data = {}
            self.request = request
            self.return_value = return_value
            self.base_serializer = PostSerializer
            self.section_serializer = SectionSerializer
            
        def get_post(self):
            return self.return_value
            
        def get_all(self):
            # get all posts from a specific user
            # => first get user's id
            
            self.return_value["request_event"] = self.request.data.get("event", None)
            self.return_value["data"] = self.base_serializer(self.query.all(), many=True).data 
            self.return_value["message"] = "All posts collected successfully!"
            
            return self.return_value
        
        def get_user_posts(self):
            user = User.objects.get(code=self.request.data.get("code"))
            posts = user.post_user.all()
            
            paginator = Paginator(posts, 10)
            
            # print(paginator.num_pages)
            
            page_number = self.request.data.get("page_number", None)
            page_posts = paginator.get_page(page_number)
            
            data = {
                "posts": self.base_serializer(page_posts, many=True).data,
                "num_pages": paginator.num_pages
            }
            
            self.return_value["request_event"] = self.request.data.get("event", None)
            self.return_value["data"] = data
            self.return_value["message"] = "All posts from you collected successfully!"
            
            return self.return_value
        
        def get_post_details(self):
            # get post 
            post = self.query.get(post_code=self.request.data.get("post_code"))
            
            # get post's sections
            sections = post.section_post.all()
            
            data = {
                post: self.base_serializer(post).data , 
                sections: self.section_serializer(sections, many=True).data
            }
       
            self.return_value["request_event"] = self.request.data.get("event", None)
            self.return_value["data"] = data
            self.return_value["message"] = "All posts from you collected successfully!"

        def get_related(self):
            self.return_value["request_event"] = self.request.data.get("event", None)
            self.return_value["data"] = self.base_serializer(self.query.all(), many=True).data 
            self.return_value["message"] = "All posts collected successfully!"
            
            return self.return_value
            
        def add_post(self):
            # set request_event
            self.return_value["event"] = self.request.data.get("event", None)
            
            # clean data from self.request
            # print(self.request.data.keys())
            
            for key in self.request.data.keys():
                self.data[key] = self.request.data.get(key, None)
            
            # add author id to data set
            self.data["post_author"] = self.data.get("id", None)
            # print(type(self.data.get("post_title", None)))
            
            post_section_keys = [key for key in self.data.keys() if "post_section" in key]
            
            
            post_section = []
            
            # print(post_section_keys)
            
            if post_section_keys:
                post_section_obj = {
                    "section_title": None,
                    "section_image": None,
                    "section_content": None,
                    "section_public": None,
                }
                
                for _ in range(int(post_section_keys[-1][-1]) + 1):
                    section_keys = [key for key in post_section_keys if str(_) in key]
                    copied = post_section_obj.copy()
                    # set data for post section
                    for key in section_keys:
                        for obj_key in post_section_obj.keys():
                            if obj_key in key:
                                if obj_key != "section_image":  
                                    copied[obj_key] = self.request.data.get(key, None)
                                else:
                                    copied[obj_key] = self.request.data.getlist(key, [])

                    post_section.append(copied)
                
                post_section_keys.sort()
                
                        
            self.data["post_section"] = post_section
            
            # remove key, value from self.data
            for key in post_section_keys:
                del self.data[key]
            
            # store data
            serializer = self.base_serializer(data=self.data)
                     
            if serializer.is_valid():
                # call to create a post base on information from request
                serializer.create(self.request)
                self.return_value["data"] = serializer.data
                self.return_value["message"] = "Data went through."
                
            else:
                print(serializer.errors)
                self.return_value["error"] = "Oops!."
                
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
        
        
        
   
    
    