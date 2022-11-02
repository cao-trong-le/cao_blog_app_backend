from django.urls import path, re_path
from . import views

urlpatterns = [
    path('posts/', views.PostView.as_view(), name="post"),
    path('posts/<str:post_code>/', views.PostView.as_view(), name="post-detail-view"),
    path('create/post/', views.PostView.as_view(), name="product-view"),
    path('sections/', views.SectionView.as_view(), name="section"),
]
