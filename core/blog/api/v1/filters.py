# filters.py
from django_filters import ModelMultipleChoiceFilter, FilterSet
from accounts.models import User
from blog.models import Post, Category


# select multiple user with click+ctrl
class PostFilter(FilterSet):
    category = ModelMultipleChoiceFilter(
        queryset=Category.objects.all(), field_name="category", to_field_name="id"
    )
    author = ModelMultipleChoiceFilter(
        queryset=User.objects.all(), field_name="author", to_field_name="id"
    )

    class Meta:
        model = Post
        fields = ["category", "author"]
