
import pytest
from app import schemas


def test_get_all_posts(authorized_client, create_test_posts):
    res = authorized_client.get("/posts/")
    #print(res.json())
    assert len(res.json())==len(create_test_posts)
    assert res.status_code == 200



def test_unAuthUser_get_all_posts(client,create_test_posts):
    res = client.get("/posts/")
    assert res.json().get('detail') == "Not authenticated"
    assert res.status_code == 401


def test_get_one_posts(authorized_client, create_test_posts):
    res = authorized_client.get(f"/posts/{create_test_posts[0].id}")
    #assert res.json().get('Post').get('title')==create_test_posts[0].title
    post = schemas.PostOut(**res.json())
    assert post.Post.title == create_test_posts[0].title
    assert res.status_code == 200

def test_unAuthUser_get_one_posts(client, create_test_posts):
    res = client.get(f"/posts/{create_test_posts[0].id}")
    assert res.json().get('detail') == "Not authenticated"
    assert res.status_code == 401

def test_get_a_post_with_invalid_id(authorized_client,create_test_posts):
    res = authorized_client.get(f"/posts/0")
    #assert res.json().get('detail') == "Not authenticated"
    assert res.status_code == 404



@pytest.mark.parametrize("title, content, published", [
    ("title1", "content1", False),
    ("title2", "content2", True)
])
def test_create_post(authorized_client, test_user,title,content, published):
    res = authorized_client.post("/posts/",
        json={
    "title":title,
    "content" :  content,
    "published": published
    }
    )
    created_post = schemas.Post(**res.json())
    #print(created_post)
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.owner_id == test_user['id']


def test_create_post_default_published_true(authorized_client, test_user):
    res = authorized_client.post("/posts/",
        json={
    "title":"111111111",
    "content" :  'qwertyyyyyyyyyyyyyyyy',
    }
    )
    created_post = schemas.Post(**res.json())
    #print(created_post)
    assert res.status_code == 201
    assert created_post.title == '111111111'
    assert created_post.owner_id == test_user['id']


def test_create_post_unAuth_user(client, test_user):
    res = client.post("/posts/",
        json={
    "title":"111111111",
    "content" :  'qwertyyyyyyyyyyyyyyyy',
    }
    )
    assert res.json().get('detail') == "Not authenticated"
    assert res.status_code == 401


def test_delete_a_post(authorized_client, test_user,create_test_posts):

    res = authorized_client.delete(f"/posts/{create_test_posts[0].id}")
    assert res.status_code == 204



def test_delete_post_unAuthUser(client, test_user,create_test_posts):
    res = client.delete(f"/posts/{create_test_posts[0].id}"
    )
    assert res.json().get('detail') == "Not authenticated"
    assert res.status_code == 401


def test_delete_a_invalid_post(authorized_client, test_user,create_test_posts):

    res = authorized_client.delete(f"/posts/0")
    assert res.status_code == 404


def test_delete_other_user_post(authorized_client,test_user,create_test_posts):
    res = authorized_client.delete(f"/posts/{create_test_posts[3].id}")
    #print(res.json())
    assert res.status_code == 403


def test_update_a_post(authorized_client,test_user,create_test_posts):
    res = authorized_client.put(f"/posts/{create_test_posts[0].id}",
        json={
    "title":"updated post",
    "content" :  'updated qwertyyyyyyyyyyyyyyyy',
    }
    )
    updated_post = schemas.Post(**res.json())
    assert updated_post.owner_id == test_user['id']
    assert updated_post.title == 'updated post'
    assert res.status_code == 200


def test_update_a_post_unAuthUser(client,test_user,create_test_posts):
    res = client.put(f"/posts/{create_test_posts[0].id}",
        json={
    "title":"updated post",
    "content" :  'updated qwertyyyyyyyyyyyyyyyy',
    }
    )
    assert res.json().get('detail') == "Not authenticated"
    assert res.status_code == 401


def test_update_a_post_of_other_User(authorized_client,test_user,create_test_posts):
    res = authorized_client.put(f"/posts/{create_test_posts[3].id}",
        json={
    "title":"updated post",
    "content" :  'updated qwertyyyyyyyyyyyyyyyy',
    }
    )
    assert res.status_code == 403
    

def test_update_a_invalid_post(authorized_client,test_user,create_test_posts):
    res = authorized_client.put(f"/posts/0",
        json={
    "title":"updated post",
    "content" :  'updated qwertyyyyyyyyyyyyyyyy',
    }
    )
    assert res.status_code == 404
     
    












