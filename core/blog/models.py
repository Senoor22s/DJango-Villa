from django.db import models
from accounts.models import User


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    price = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to="blog/", default="blog/property-01.jpg")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ManyToManyField("Category")
    status = models.BooleanField(default=False)
    login_require = models.BooleanField(default=False)
    counted_view = models.PositiveIntegerField(default=0)
    published_date = models.DateTimeField(null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_date"]

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
