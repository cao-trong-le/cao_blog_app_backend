from django.urls import path, re_path
from . import views

urlpatterns = [
    path('posts/<str:key>/', views.PostView.as_view(), name="product-view"),
    path('create/post/', views.PostView.as_view(), name="product-view"),
]
