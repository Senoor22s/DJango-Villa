import pytest
from django.urls import reverse
from django.utils import timezone
from accounts.models import User
from blog.models import Post, Category


@pytest.mark.django_db
def test_post_list_view(client):
    url = reverse("blog:posts")
    response = client.get(url)
    assert response.status_code == 200
    assert "posts" in response.context


@pytest.mark.django_db
def test_post_list_by_category(client):
    cat = Category.objects.create(name="django")
    user = User.objects.create_user(email="fa@mail.com", password="pass")
    p = Post.objects.create(
        title="T",
        content="...",
        author=user,
        status=True,
        published_date=timezone.now(),
    )
    p.category.add(cat)
    url = reverse("blog:category", kwargs={"cat_name": cat.name})
    response = client.get(url)
    assert response.status_code == 200
    assert "posts" in response.context
    assert p in response.context["posts"]


@pytest.mark.django_db
def test_post_detail_redirects_not_logged_in(client):
    user = User.objects.create_user(email="foo@mail.com", password="bar")
    cat = Category.objects.create(name="api")
    post = Post.objects.create(
        title="D1",
        content="CT",
        author=user,
        status=True,
        published_date=timezone.now(),
    )
    post.category.add(cat)
    url = reverse("blog:post-detail", kwargs={"pk": post.pk})
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_post_detail_logged_in(client):
    user = User.objects.create_user(email="foo@mail.com", password="bar")
    cat = Category.objects.create(name="api")
    post = Post.objects.create(
        title="Logged",
        content="CT",
        author=user,
        status=True,
        published_date=timezone.now(),
    )
    post.category.add(cat)
    client.login(email="foo@mail.com", password="bar")
    url = reverse("blog:post-detail", kwargs={"pk": post.pk})
    response = client.get(url)
    assert response.status_code == 200
    assert "post" in response.context
    assert response.context["post"] == post


@pytest.mark.django_db
def test_counted_view_increment(client):
    user = User.objects.create_user(email="foo@mail.com", password="bar")
    cat = Category.objects.create(name="api")
    post = Post.objects.create(
        title="Logged",
        content="CT",
        author=user,
        status=True,
        published_date=timezone.now(),
    )
    post.category.add(cat)
    client.login(email="foo@mail.com", password="bar")
    url = reverse("blog:post-detail", kwargs={"pk": post.pk})

    client.get(url)
    post.refresh_from_db()
    initial = post.counted_view

    client.get(url)
    post.refresh_from_db()
    assert post.counted_view == initial + 1
