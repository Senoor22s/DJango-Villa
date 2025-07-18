from django.urls import path, include
from . import views

app_name = "comment"

urlpatterns = [
    path("contact/", views.ContactPage.as_view(), name="contact"),
]
