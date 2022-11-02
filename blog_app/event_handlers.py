from .serializers import (
    ImageSerializer,
    PostSerializer, 
    PostDataSerializer,
    SectionDataSerializer,
    SectionSerializer, 
    CommentSerializer, 
    ReplySerializer,
    FileSerializer,
)
from .models import File, Image, Post, Section, Comment, Reply
from django.contrib.auth import get_user_model
from rest_framework import status

import json

from django.core.paginator import Paginator
from ast import literal_eval




User = get_user_model()

class EventHandler:
    def __init__ (self, request):
        self.data = request.data
        self.request = request
        self.return_value = {
            "event": None,
            "data": None,
            "message": None,
            "status": None
        }
        # self.base_event_handler = self.BaseEventHandler(request, self.return_value)
        self.post_event_handler = self.PostEventHandler(request, self.return_value)
        self.section_event_handler = self.SectionEventHandler(request, self.return_value)
    
    class PostEventHandler:   
        def __init__(self, request, return_value):
            self.query = Post.objects
            self.data = {}
            self.request = request
            self.return_value = return_value
            self.post_data_serializer = PostDataSerializer
            self.base_serializer = PostSerializer
            self.section_serializer = SectionSerializer
            self.image_serializer = ImageSerializer
            
        def get_post(self):
            return self.return_value
        
        def get_post_by(self):
            
            
            return self.return_value
            
        def get_all_posts(self):
            # get all posts from a specific user
            # => first get user's id
            user = User.objects.get(code=self.request.data.get("code"))
            posts = user.post_user.all()
            
            self.return_value["request_event"] = self.request.data.get("event", None)
            self.return_value["posts"] = self.post_data_serializer(posts, many=True).data 
            self.return_value["message"] = "All posts collected successfully!"
            
            return self.return_value
        
        def filter_posts(self):
            keyword = self.request.data.get("keyword", None)
            date = str(self.request.data.get("date", None))
            month = str(self.request.data.get("month", None))
            year = str(self.request.data.get("year", None))
            page = str(self.request.data.get("page_number", None))
            user_code = self.request.data.get("user_code", None)
            posts = None
            
            query = {}
            query["post_title__icontains"] = keyword
            
            if user_code != "":
                user = User.objects.get(code=user_code)
                query["post_author"] = user
            if date:
                query["post_date__date"] = date
            if month:
                query["post_date__month"] = month
            if year:
                query["post_date__year"] = year
                
            try:
                posts = self.query.filter(**query)
            
                paginator = Paginator(posts, 5)
            
                # page_number = self.request.data.get("page_number", None)
                page_posts = paginator.get_page(page)
                
                # attach images to each post
                returned_posts = self.post_data_serializer(page_posts, many=True).data
                
                data = {
                    "posts": returned_posts,
                    "num_pages": paginator.num_pages
                }
                    
                self.return_value["request_event"] = self.request.data.get("event", None)
                self.return_value["data"] = data
                self.return_value["message"] = "All posts from you collected successfully!"
                self.return_value["status"] = status.HTTP_200_OK
                
            except ValueError as e:
                print(e)
                self.return_value["message"] = "Oops !"
                self.return_value["status"] = status.HTTP_400_BAD_REQUEST
            
            return self.return_value
        
        def get_user_posts(self):
            user = User.objects.get(code=self.request.data.get("code"))
            posts = user.post_user.all()
            
            # print(posts[0].section_post.all()[0].section_image.all())
            
            paginator = Paginator(posts, 5)
        
            page_number = self.request.data.get("page_number", None)
            page_posts = paginator.get_page(page_number)
            
            
            # attach images to each post
            returned_posts = self.post_data_serializer(page_posts, many=True).data
              
            data = {
                "posts": returned_posts,
                "num_pages": paginator.num_pages
            }
            
            self.return_value["request_event"] = self.request.data.get("event", None)
            self.return_value["data"] = data
            self.return_value["message"] = "All posts from you collected successfully!"
            
            return self.return_value
        
        def add_post(self):
            # set request_event
            self.return_value["event"] = self.request.data.get("event", None)
            
            # clean data from self.request and set it to self.data
            # post data => object
            original_post = json.loads(self.request.data.get("post", None))
            
            # original post
            original_post["post_image"] = []
            
            # valid post 
            # user = User.objects.get(id=int(self.request.data.get("id", None)))
            valid_post = {**original_post}
            valid_post["post_image"] = None
            valid_post["post_author"] = self.request.data.get("id", None)
            valid_post["post_public"] = bool(original_post["post_public"])
            valid_post["post_edited"] = bool(original_post["post_edited"])
              
            # section data => [objects]
            
            # original data
            original_sections = []
            # valid data
            valid_sections = []
            raw_sections = self.request.data.getlist("section", [])
            
            for raw_section in raw_sections:
                original_section = json.loads(raw_section)
                original_section["section_image"] = []
                del original_section["section_id"]
                original_sections.append(original_section)
                
                # append to valid data
                valid_section = {**original_section}
                valid_section["section_image"] = None
                valid_section["section_public"] = bool(original_section["section_public"])
                valid_sections.append(valid_section)
                
            # set post_image back
            images = self.request.data.getlist("images", [])
            
            for image in images:
                if "post" in image.name:
                    original_post["post_image"].append(image)
                
                if "section" in image.name:
                    name_paths = image.name.split("_")
                    # print(name_paths)
                    original_sections[int(name_paths[1])]["section_image"].append(image)
                    
    
            # store data
            serializer = self.base_serializer(data={**valid_post})
                     
            if serializer.is_valid():
                # call to create a post base on information from request
                serializer.create(original_post, original_sections)
                self.return_value["data"] = serializer.data
                self.return_value["message"] = "Data went through."
                
            else:
                print(serializer.errors)
                self.return_value["error"] = "Oops!."
             
            return self.return_value

        def delete_many_posts(self):
            # convert a string list to a iterative list
            post_codes = literal_eval(self.request.data.get("post_codes", None))
       
            # delete selected posts
            self.return_value["request_event"] = self.request.data.get("event", None)
            
            try:
                posts = User.objects.get(code=self.request.data.get("user_code")).post_user.all()
                posts = posts.filter(post_code__in=post_codes)
                posts.delete()
                
                self.return_value["message"] = "Seleceted posts are deleted successfully!"
                self.return_value["status"] = status.HTTP_204_NO_CONTENT
            except Exception as e:
                self.return_value["message"] = "Oops! Your request post has not been found!"
                self.return_value["status"] = status.HTTP_400_BAD_REQUEST
                
            return self.return_value
    
        def delete_all_posts(self):
            try:
                posts = User.objects.get(code=self.request.data.get("user_code")).post_user.all()
            except Exception as e:
                self.return_value["message"] = "Invalid User"
                self.return_value["status"] = status.HTTP_400_BAD_REQUEST
            
            try:
                if len(posts) > 0:
                    posts.delete()
                    self.return_value["message"] = "All posts are deleted successfully!"
                    self.return_value["status"] = status.HTTP_200_OK
                else:
                    # self.return_value["message"] = "You don't have any post"
                    self.return_value["status"] = status.HTTP_204_NO_CONTENT
                    
            except Exception as e:
                self.return_value["message"] = "Internal Error"
                self.return_value["status"] = status.HTTP_400_BAD_REQUEST
            
            return self.return_value
            
        def edit_post(self):
            # set request_event
            self.return_value["event"] = self.request.data.get("event", None)
            
            # clean data from self.request and set it to self.data
            # post data => object
            original_post = json.loads(self.request.data.get("post", None))
            
            # original post
            original_post["post_image"] = []
            
            # valid post 
            # user = User.objects.get(id=int(self.request.data.get("id", None)))
            valid_post = {**original_post}
            valid_post["post_image"] = None
            valid_post["post_author"] = self.request.data.get("id", None)
            valid_post["post_public"] = bool(original_post["post_public"])
            valid_post["post_edited"] = bool(original_post["post_edited"])
              
            # section data => [objects]
            
            # original data
            original_sections = []
            # valid data
            valid_sections = []
            raw_sections = self.request.data.getlist("section", [])
            
            for raw_section in raw_sections:
                original_section = json.loads(raw_section)
                original_section["section_image"] = []
                del original_section["section_id"]
                original_sections.append(original_section)
                
                # append to valid data
                valid_section = {**original_section}
                valid_section["section_image"] = None
                valid_section["section_public"] = bool(original_section["section_public"])
                valid_sections.append(valid_section)
                
        
            # call to create a post base on information from request
            try:
                self.base_serializer({**valid_post}).create(original_post, original_sections)
                self.return_value["data"] = self.base_serializer.data
                self.return_value["message"] = ""
                self.return_value["status"] = status.HTTP_202_ACCEPTED
                
            except ValueError as v:
                self.return_value["message"] = ""
                self.return_value["status"] = status.HTTP_400_BAD_REQUEST
            
            return self.return_value
        
        def delete_post_heading_image(self):
            self.return_value["event"] = self.request.data.get("event", None)
            
            # get image code
            image_code = self.request.data.get("image_code", None)
            image = Image.objects.filter(image_code=image_code)
            
            if image.exists():
                image[0].delete()
                self.return_value["message"] = f"Heading image has been removed successfully"
                self.return_value["status"] = status.HTTP_204_NO_CONTENT
                
            else:
                self.return_value["message"] = f"Heading image does not exist."
                self.return_value["error"] = "Not Found"
                self.return_value["status"] = status.HTTP_400_BAD_REQUEST
                    
            return self.return_value
        
        def add_post_heading_image(self):
            self.return_value["event"] = self.request.data.get("event", None)
            
            # get image code
            post_code = self.request.data.get("post_code", None)
            new_heading_image = self.request.data.get("new_image", None)
            
            try:
                if post_code:
                    post = self.query.get(post_code=post_code)
                    input_data = {
                        "image_related_post": post,
                        "image_content": new_heading_image
                    }
                    created_image = Image(**input_data)
                    created_image.save()
                
                self.return_value["image"] = self.image_serializer(created_image).data
                self.return_value["message"] = f"Heading image is added successfully"
                self.return_value["status"] = status.HTTP_200_OK
                
            except ValueError as e:
                self.return_value["message"] = f"The heading image is failed to be added."
                self.return_value["status"] = status.HTTP_400_BAD_REQUEST
                    
            return self.return_value
        
        def update_post_heading_image(self):
            self.return_value["event"] = self.request.data.get("event", None)
            
            # get image code
            image_code = self.request.data.get("image_code", None)
            new_heading_image = self.request.data.get("new_image", None)
            image = Image.objects.get(image_code=image_code)
            
            try:
                image.image_content.delete(save=False)
                image.image_content = new_heading_image
                image.save()
                
                self.return_value["image"] = self.image_serializer(image).data
                self.return_value["message"] = f"Heading image is updated successfully"
                self.return_value["status"] = status.HTTP_200_OK
                    
            except ValueError as e:
                print(e)
                self.return_value["message"] = f"Heading image {image_code} does not exist."
                self.return_value["error"] = "Not Found"
                self.return_value["status"] = status.HTTP_204_NO_CONTENT
                
            return self.return_value
        
        def add_post_heading(self):
            pass
        
        # update text fields
        def update_post_heading(self):
            self.return_value["event"] = self.request.data.get("event", None)
            
            # get post code
            post_code = self.request.data.get("post_code", None)
            post = self.query.get(post_code=post_code)
            
            serializer = self.base_serializer(post)
            
            try:
                serializer.update(self.request)
                self.return_value["message"] = f"Heading is updated successfully"
                self.return_value["status"] = status.HTTP_202_ACCEPTED
                
            except Exception as e:
                print(e)
                self.return_value["message"] = "Internal Bug"
                self.return_value["status"] = status.HTTP_400_BAD_REQUEST
                    
            return self.return_value
        
        def create_post(self):
            request_data = self.request.data
            self.return_value["event"] = request_data.get("event", None)
            
            # get post title
            post_title = request_data.get("post_title", None)
            
            # get author
            author_code = request_data.get("user_code", None)
            post_author = User.objects.get(code=author_code)
            
            input_data = {
                "post_title": post_title,
                "post_author": post_author
            }
            
            post = Post(**input_data)
            post.save()
            
            serializer = self.post_data_serializer(post)
            
            try:
                self.return_value["post"] = serializer.data
                self.return_value["message"] = f"Heading is updated successfully"
                self.return_value["status"] = status.HTTP_201_CREATED
                
            except Exception as e:
                self.return_value["message"] = "Internal Bug"
                self.return_value["status"] = status.HTTP_400_BAD_REQUEST
                    
            return self.return_value
        
        def save_new_post(self):
            request_data = self.request.data
            self.return_value["event"] = request_data.get("event", None)
            
            # get post
            post_code = request_data.get("post_code")
            post = self.query.get(post_code=post_code)
            
            updated_post = self.base_serializer(post).save_new_post()
            
            try:
                self.return_value["post"] = self.post_data_serializer(updated_post).data
                self.return_value["message"] = "The new post has been saved successfully."
                self.return_value["status"] = status.HTTP_200_OK
                
            except ValueError as e:
                print(e)
                self.return_value["message"] = "Internal Bug"
                self.return_value["status"] = status.HTTP_400_BAD_REQUEST
            
            return self.return_value
            
    class SectionEventHandler:   
        def __init__(self, request, return_value):
            self.query = Section.objects
            self.data = request.data
            self.request = request
            self.return_value = return_value
            self.base_serializer = SectionSerializer
            self.post_data_serializer = PostDataSerializer
            self.section_data_serializer = SectionDataSerializer
            self.image_serializer = ImageSerializer
            self.file_serializer = FileSerializer
        
        def add_section(self):
            # set request_event
            self.return_value["event"] = self.request.data.get("event", None)
            
            # print({**self.data}.get("base_price"))
            # print(self.data.get("base_group"))
            
            # store data
            section_author = User.objects.get(code=self.request.data.get("user_code"))
            section_post = Post.objects.get(post_code=self.request.data.get("post_code"))
            section_title = self.request.data.get("section_title", None)
            
            input_data = {
                "section_author": section_author,
                "section_post": section_post,
                "section_title": section_title
            }
            
            try:
                section = Section(**input_data)
                section.save()
                # print(section)
                
                self.return_value["section"] = self.section_data_serializer(section).data
                self.return_value["message"] = "A new section has been created"
                self.return_value["status"] = status.HTTP_201_CREATED
            except Exception as e:
                self.return_value["message"] = "Internal Error"
                self.return_value["status"] = status.HTTP_400_BAD_REQUEST
                
            return self.return_value
            
        def delete_section(self):
            self.return_value["event"] = self.request.data.get("event", None)
            
            try:
                section_code = self.request.data.get("section_code", None)
                section = self.query.get(base_code=section_code)
                serializer = self.base_serializer(section)
                serializer.delete_section()
                
                self.return_value["message"] = "The section has been deleted successfully."
                self.return_value["status"] = status.HTTP_202_ACCEPTED
                
            except ValueError as e:
                self.return_value["message"] = "The item does not exist."
                self.return_value["error"] = "Not Found"
                self.return_value["status"] = status.HTTP_204_NO_CONTENT
                
            return self.return_value
      
        def delete_sections(self):
            self.return_value["request_event"] = self.request.data.get("event", None)
            section_codes = self.request.data.getlist("section_code", [])
            sections = self.query.filter(section_code__in=section_codes)
            
            if sections.exists():
                try:
                    sections.delete()
                    self.return_value["message"] = "The sections have been deleted successfully."
                    self.return_value["status"] = status.HTTP_202_ACCEPTED
                    
                except ValueError as e:
                    print(e)
                    self.return_value["message"] = "The sections have been deleted successfully."
                    self.return_value["status"] = status.HTTP_400_BAD_REQUEST
                    
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
             
        def update_section(self):
            print(self.request.data)
            # print(eval(self.request.data.get("section_public")))
            # print(bool(self.request.data.get("section_public")))
            
            # set request_event
            self.return_value["event"] = self.request.data.get("event", None)
            
            # get section
            section_code = self.request.data.get("section_code", None)
            section = self.query.get(section_code=section_code)
            post = section.section_post
            serializer = self.base_serializer(section)
            
            request_data = {}
            
            for key in self.request.data:
                request_data[key] = self.request.data[key]
                
            try:
                section = serializer.update_content(request_data)
                print(self.section_data_serializer(section).data)
                self.return_value["post"] = self.post_data_serializer(post).data
                self.return_value["section"] = self.section_data_serializer(section).data
                self.return_value["message"] = "Data went through."
                self.return_value["status"] = status.HTTP_202_ACCEPTED
                
            except Exception as e:
                self.return_value["message"] = "The items do not exist."
                self.return_value["error"] = "Not Found"
                self.return_value["status"] = status.HTTP_204_NO_CONTENT
                  
            return self.return_value
        
        def add_section_images(self):
            # print("running !!!")
            # print(self.request.data.getlist("section_image"))
            self.return_value["event"] = self.request.data.get("event", None)
            
            # get image code
            section = self.query.get(section_code=self.request.data.get("section_code"))
            
            post = section.section_post
            
            try:
                section_instance = self.base_serializer(section).add_images(self.request)
                section_data = self.section_data_serializer(section_instance).data
                self.return_value["post"] = self.post_data_serializer(post).data
                self.return_value["section"] = section_data
                self.return_value["message"] = "Section images are added successfully"
                self.return_value["status"] = status.HTTP_201_CREATED
                
            except ValueError as error:
                print(error)
                self.return_value["message"] = "Oops! ..."
                self.return_value["status"] = status.HTTP_400_BAD_REQUEST
                
            return self.return_value
        
        def update_section_image(self):
            self.return_value["event"] = self.request.data.get("event", None)
            
            # get image code
            try:
                image_code = self.request.data.get("image_code", None)
                new_image = self.request.data.get("new_image", None)
                image = Image.objects.get(image_code=image_code)
                serializer = self.image_serializer(image)
                
                section = serializer.update_section_image(new_image).image_related_section
                
                self.return_value["image"] = serializer.data
                self.return_value["section"] = self.section_data_serializer(section).data
                self.return_value["post"] = self.post_data_serializer(section.section_post).data
                self.return_value["message"] = f"Section image {image_code} is updated successfully"
                self.return_value["status"] = status.HTTP_202_ACCEPTED
                
            except ValueError as e:
                print(e)
                self.return_value["message"] = f"Section image {image_code} does not exist."
                self.return_value["error"] = "Not Found"
                self.return_value["status"] = status.HTTP_400_BAD_REQUEST
                    
            return self.return_value
        
        def remove_section_image(self):
            self.return_value["event"] = self.request.data.get("event", None)
            
            # get image code
            image_code = self.request.data.get("image_code", None)
            image = Image.objects.get(image_code=image_code)
            section = image.image_related_section
            post = section.section_post
            serializer = self.image_serializer(image)
            
            print(self.section_data_serializer(section).data)
            
            try:
                serializer.delete_section_image()
                self.return_value["section"] = self.section_data_serializer(section).data
                self.return_value["post"] = self.post_data_serializer(post).data
                self.return_value["message"] = "Section image is removed successfully"
                self.return_value["status"] = status.HTTP_202_ACCEPTED
                
            except ValueError as e:
                print(e)
                self.return_value["message"] = "Section image does not exist."
                self.return_value["error"] = "Not Found"
                self.return_value["status"] = status.HTTP_400_BAD_REQUEST
                    
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
        
        def add_section_files(self):
            # print("running !!!")
            
            print(self.request.data.getlist("section_file")[0].name)
            # print(self.request.data.getlist("section_image"))
            self.return_value["event"] = self.request.data.get("event", None)
            
            # get image code
            section = self.query.get(section_code=self.request.data.get("section_code"))
            
            post = section.section_post
            
            try:
                section_instance = self.base_serializer(section).add_files(self.request)
                section_data = self.section_data_serializer(section_instance).data
                self.return_value["post"] = self.post_data_serializer(post).data
                self.return_value["section"] = section_data
                self.return_value["message"] = "Section files are added successfully"
                self.return_value["status"] = status.HTTP_201_CREATED
                
            except ValueError as error:
                print(error)
                self.return_value["message"] = "Oops! ..."
                self.return_value["status"] = status.HTTP_400_BAD_REQUEST
                
            return self.return_value
        
        def update_section_file(self):
            self.return_value["event"] = self.request.data.get("event", None)
            
            # get image code
            try:
                file_code = self.request.data.get("file_code", None)
                new_file = self.request.data.get("new_file", None)
                file = File.objects.get(file_code=file_code)
                serializer = self.file_serializer(file)
                
                section = serializer.update_section_file(new_file).file_related_section
                
                self.return_value["image"] = serializer.data
                self.return_value["section"] = self.section_data_serializer(section).data
                self.return_value["post"] = self.post_data_serializer(section.section_post).data
                self.return_value["message"] = f"The section file has been updated successfully"
                self.return_value["status"] = status.HTTP_202_ACCEPTED
                
            except ValueError as e:
                print(e)
                self.return_value["message"] = f"Section file does not exist."
                self.return_value["error"] = "Not Found"
                self.return_value["status"] = status.HTTP_400_BAD_REQUEST
                    
            return self.return_value
        
        def remove_section_file(self):
            self.return_value["event"] = self.request.data.get("event", None)
            
            # get file code
            file_code = self.request.data.get("file_code", None)
            file = File.objects.get(file_code=file_code)
            section = file.file_related_section
            post = section.section_post
            serializer = self.file_serializer(file)
            
            # print(self.section_data_serializer(section).data)
            
            try:
                serializer.delete_section_file()
                self.return_value["section"] = self.section_data_serializer(section).data
                self.return_value["post"] = self.post_data_serializer(post).data
                self.return_value["message"] = "Section file is removed successfully"
                self.return_value["status"] = status.HTTP_202_ACCEPTED
                
            except ValueError as e:
                print(e)
                self.return_value["message"] = "Section file does not exist."
                self.return_value["error"] = "Not Found"
                self.return_value["status"] = status.HTTP_400_BAD_REQUEST
                    
            return self.return_value
        
   
    
    