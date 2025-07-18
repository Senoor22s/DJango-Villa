from django.urls import path, include
from . import views

app_name = "blog"

urlpatterns = [
    path("posts/", views.PostList.as_view(), name="posts"),
    path("post/<int:pk>", views.PostDetail.as_view(), name="post-detail"),
    path("Category/<str:cat_name>", views.PostList.as_view(), name="category"),
    path("api/v1/", include("blog.api.v1.urls", namespace="api-v1")),
]
