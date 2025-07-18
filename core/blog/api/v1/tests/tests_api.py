import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from accounts.models import User
from blog.models import Category, Post
from django.utils import timezone


@pytest.fixture
def user_api():
    return User.objects.create_user(email="apiuser@mail.com", password="1234")


@pytest.fixture
def category_api():
    return Category.objects.create(name="ApiCat")


@pytest.mark.django_db
def test_list_posts_api(user_api, category_api):
    post = Post.objects.create(
        title="Test",
        content="Test Content",
        author=user_api,
        status=True,
        published_date=timezone.now(),
    )
    post.category.add(category_api)
    client = APIClient()
    url = reverse("blog:api-v1:posts-list")
    response = client.get(url)
    assert response.status_code == 200
    assert post.title in str(response.data)


@pytest.mark.django_db
def test_create_post_api(user_api, category_api):
    client = APIClient()
    client.force_authenticate(user=user_api)
    url = reverse("blog:api-v1:posts-list")
    data = {
        "title": "NewAPI",
        "content": "test-content",
        "category": [category_api.id],
        "status": True,
        "published_date": timezone.now(),
    }
    response = client.post(url, data, format="json")
    assert response.status_code == 201
    assert Post.objects.filter(title="NewAPI").count() == 1


@pytest.mark.django_db
def test_update_post_api(user_api, category_api):
    post = Post.objects.create(
        title="Update",
        content="update me",
        author=user_api,
        published_date=timezone.now(),
        status=True,
    )
    post.category.add(category_api)
    client = APIClient()
    client.force_authenticate(user=user_api)
    url = reverse("blog:api-v1:posts-detail", kwargs={"pk": post.id})
    data = {"title": "Updated Title", "category": [category_api.id]}
    response = client.patch(url, data, format="json")
    assert response.status_code == 200
    post.refresh_from_db()
    assert post.title == "Updated Title"


@pytest.mark.django_db
def test_delete_post_api(user_api, category_api):
    post = Post.objects.create(
        title="Del",
        content="will delete",
        author=user_api,
        published_date=timezone.now(),
        status=True,
    )
    post.category.add(category_api)
    client = APIClient()
    client.force_authenticate(user=user_api)
    url = reverse("blog:api-v1:posts-detail", kwargs={"pk": post.id})
    response = client.delete(url)
    assert response.status_code == 204
    assert not Post.objects.filter(id=post.id).exists()


@pytest.mark.django_db
def test_permissions(user_api, category_api):
    post = Post.objects.create(
        title="Secure",
        content="...",
        author=user_api,
        published_date=timezone.now(),
        status=True,
    )
    post.category.add(category_api)
    client = APIClient()
    url = reverse("blog:api-v1:posts-detail", kwargs={"pk": post.id})
    data = {"title": "NoPerm"}
    response = client.patch(url, data)
    assert response.status_code in [401, 403]
