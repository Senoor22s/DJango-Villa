import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def user_data():
    return {
        "email": "apiuser1@example.com",
        "password": "myStrongPass!123",
        "password1": "myStrongPass!123",
    }


@pytest.mark.django_db
def test_api_registration(client, user_data):
    url = reverse("accounts:api-v1:registration")
    res = client.post(url, user_data)
    print("REG ERRORS:", res.json())
    assert res.status_code == 201
    assert User.objects.filter(email=user_data["email"]).exists()


@pytest.mark.django_db
def test_api_login_and_token(client, user_data):
    user = User.objects.create_user(
        email=user_data["email"], password=user_data["password"], is_verified=True
    )
    url = reverse("accounts:api-v1:token-login")
    res = client.post(
        url, {"email": user_data["email"], "password": user_data["password"]}
    )
    assert res.status_code == 200
    assert "token" in res.json() or "access" in res.json()


@pytest.mark.django_db
def test_api_change_password(client, user_data):
    user = User.objects.create_user(
        email=user_data["email"], password="old_password", is_verified=True
    )
    client.force_login(user)
    url = reverse("accounts:api-v1:change-password")
    payload = {
        "old_password": "old_password",
        "new_password": "newSecretPassword!123",
        "new_password1": "newSecretPassword!123",
    }
    res = client.put(url, payload, content_type="application/json")
    print("CHPASS ERRORS:", res.json())
    assert res.status_code == 200
    user.refresh_from_db()
    assert user.check_password("newSecretPassword!123")


@pytest.mark.django_db
def test_api_activation(client, user_data, settings):
    import jwt

    user = User.objects.create_user(
        email=user_data["email"], password=user_data["password"], is_verified=False
    )
    payload = {"user_id": user.id}
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    url = reverse("accounts:api-v1:confirm-activation", kwargs={"token": token})
    res = client.get(url)
    assert res.status_code == 200
    user.refresh_from_db()
    assert user.is_verified is True


@pytest.mark.django_db
def test_api_reset_password(client, user_data):
    user = User.objects.create_user(
        email=user_data["email"], password="old-password", is_verified=True
    )
    url = reverse("accounts:api-v1:reset-password")
    res = client.post(url, {"email": user.email})
    assert res.status_code == 200


@pytest.mark.django_db
def test_api_confirm_reset_password(client, user_data, settings):
    import jwt

    user = User.objects.create_user(
        email=user_data["email"], password="old-password", is_verified=True
    )
    payload = {"user_id": user.id}
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    url = reverse("accounts:api-v1:confirm-reset-password", kwargs={"token": token})

    new_password = "finalNewPassword123!@#"
    payload = {"new_password": new_password, "new_password1": new_password}
    res = client.put(url, payload, content_type="application/json")
    print("CONFIRM RESET ERRORS:", res.json())
    assert res.status_code == 200

    user.refresh_from_db()
    assert user.check_password(new_password)
