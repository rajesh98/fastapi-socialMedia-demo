import json
from app import schemas
#from .database_test import client,session
import pytest
from jose import jwt 
from app.config import settings








# def test_root(client):
#     res = client.get("/")
#     assert res.json().get('Hello')=="World"
#     assert res.status_code == 200


def test_create_user(client):
    res = client.post(
        "/users/",json={
    "email": "testuser1@gmmail.com",
    "password" : "12345"
    }
    )
    user_out = schemas.UserOut(**res.json())
    assert user_out.email=="testuser1@gmmail.com"
    assert res.status_code == 201


def test_login(client,test_user):
    res = client.post("/login",
        data={
    "username": test_user['email'],
    "password" :  test_user['password']
    }
    )
    login_token = schemas.Token(**res.json())

    payload = jwt.decode(login_token.access_token,settings.secret_key,algorithms=settings.algorithim)
    id:str = payload.get("user_id")
    assert id== test_user['id']
    assert login_token.token_type ==  'bearer'
    assert res.status_code == 200




@pytest.mark.parametrize("username, password, status_code", [
    ('rajwrong@gmail.com','correct_pass',403),
    ('rajcorrect@gmail.com','wrong_pass',403),
    (None,'correct_pass',422),
    ('rajcorrect@gmail.com',None,422),

])
def test_incorrect_login(client,test_user, username, password, status_code):
    res = client.post("/login",
        data={
    "username":username,
    "password" :  password
    }
    )
    assert res.status_code == status_code
    




