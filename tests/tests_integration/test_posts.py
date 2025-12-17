import pytest
from app import schemas


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts")

    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200
    for post in res.json():
        schemas.PostOutput(**post)


def test_unauthorized_user_get_all_posts(client):
    res = client.get("/posts")
    assert res.status_code == 401


def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_get_one_nonexistent_post(authorized_client, test_posts):
    nonexistent_id = max(p.id for p in test_posts) + 100
    res = authorized_client.get(f"/posts/{nonexistent_id}")
    assert res.status_code == 404


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOutput(**res.json())

    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content
    assert post.Post.title == test_posts[0].title
    assert res.status_code == 200


@pytest.mark.parametrize(
    "title, content, published",
    [
        ("awesome new title", "awesome new content", True),
        ("favorite pizza", "i love pepperoni", False),
        ("tallest skyscrapers", "wahoo", True),
    ],
)
def test_create_post(authorized_client, test_user, title, content, published):
    res = authorized_client.post(
        f"/posts/", json={"title": title, "content": content, "published": published}
    )
    created_post = schemas.PostResponse(**res.json())

    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.user_id == test_user["id"]


def test_create_post_default_published_true(authorized_client, test_user):
    data = {"title": "test title", "content": "test"}
    res = authorized_client.post("/posts/", json=data)
    created_post = schemas.PostResponse(**res.json())

    assert res.status_code == 201
    assert created_post.title == data["title"]
    assert created_post.content == data["content"]
    assert created_post.published == True
    assert created_post.user_id == test_user["id"]


def test_unauthorized_user_create_post(client):
    data = {"title": "test title", "content": "test"}
    res = client.post("/posts/", json=data)
    assert res.status_code == 401


def test_unauthorized_user_delete_post(client, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_delete_post_success(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204


def test_delete_post_non_exist(authorized_client, test_posts):
    nonexistent_id = max(p.id for p in test_posts) + 100
    res = authorized_client.delete(f"/posts/{nonexistent_id}")
    assert res.status_code == 404


def test_delete_other_user_post(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403


def test_unauthorized_user_update_post(client, test_posts):
    res = client.put(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_update_post(authorized_client, test_posts):
    data = {"title": "updated title", "content": "updatd content"}
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.PostResponse(**res.json())

    assert res.status_code == 200
    assert updated_post.title == data["title"]
    assert updated_post.content == data["content"]


def test_update_other_user_post(authorized_client, test_posts):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_posts[3].id,
    }
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)

    assert res.status_code == 403


def test_update_nonexistent_post(authorized_client, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[3].id,
    }
    nonexistent_id = max(p.id for p in test_posts) + 100
    res = authorized_client.put(f"/posts/{nonexistent_id}", json=data)

    assert res.status_code == 404
