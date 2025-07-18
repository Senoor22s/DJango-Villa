import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_signup_view_get(client):
    url = reverse("accounts:signup")
    response = client.get(url)
    assert response.status_code == 200
    assert b"<form" in response.content


@pytest.mark.django_db
def test_signup_view_post(client):
    url = reverse("accounts:signup")
    data = {
        "email": "user1@example.com",
        "password1": "12345strongTest",
        "password2": "12345strongTest",
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert User.objects.filter(email="user1@example.com").exists()
