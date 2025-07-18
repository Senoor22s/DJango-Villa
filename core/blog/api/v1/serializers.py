from rest_framework import serializers
from ...models import Post, Category
from django.urls import reverse


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ["id", "name"]


class PostSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, allow_null=True)
    snippet = serializers.ReadOnlyField(source="get_snippet")
    relative_url = serializers.URLField(source="get_absolute_api_url", read_only=True)
    absolute_url = serializers.SerializerMethodField()
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), many=True, write_only=True, required=False
    )
    category_detail = CategorySerializer(source="category", many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "image",
            "author",
            "content",
            "snippet",
            "status",
            "category",
            "category_detail",
            "title",
            "price",
            "login_require",
            "relative_url",
            "absolute_url",
            "created_date",
            "published_date",
        ]
        read_only_fields = ["author"]

    def get_absolute_url(self, obj):
        request = self.context.get("request")
        relative_url = reverse("blog:api-v1:posts-detail", kwargs={"pk": obj.id})
        return request.build_absolute_uri(relative_url)

    def create(self, validated_data):
        categories = validated_data.pop("category", [])
        validated_data["author"] = self.context["request"].user
        post = super().create(validated_data)
        post.category.set(categories)
        return post

    def update(self, instance, validated_data):
        categories = validated_data.pop("category", None)
        post = super().update(instance, validated_data)
        if categories is not None:
            post.category.set(categories)
        return post
