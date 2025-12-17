import pytest
import jwt
from app import schemas

from app.config import settings


def test_create_user(client):
    res = client.post("/users", json={"email": "test@gmail.com", "password": "111"})
    new_user = schemas.UserResponse(**res.json())

    assert new_user.email == "test@gmail.com"
    assert res.status_code == 201


def test_create_user_duplicate_email(client):
    user_data = {"email": "test@gmail.com", "password": "111"}

    res1 = client.post("/users", json=user_data)
    assert res1.status_code == 201

    res2 = client.post("/users", json=user_data)

    assert res2.status_code == 409
    assert res2.json()["detail"] == "Email already registered"


def test_login_user(test_user, client):
    res = client.post(
        "/login",
        data={"username": test_user["email"], "password": test_user["password"]},
    )
    login_res_token = schemas.Token(**res.json())
    payload = jwt.decode(
        login_res_token.access_token,
        settings.secret_key,
        algorithms=[settings.algorithm],
    )
    user_id = payload.get("user_id")

    assert user_id == test_user["id"]
    assert login_res_token.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("wrongemail@gmail.com", "password123", 403),
        ("sanjeev@gmail.com", "wrongpassword", 403),
        ("wrongemail@gmail.com", "wrongpassword", 403),
        (None, "password123", 422),
        ("sanjeev@gmail.com", None, 422),
    ],
)
def test_incorrect_login(client, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})

    assert res.status_code == status_code
