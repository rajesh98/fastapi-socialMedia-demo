from app import models
import pytest


@pytest.fixture()
def create_a_vote(test_user, session,create_test_posts):
    new_vote = models.Vote(post_id = create_test_posts[3].id, user_id = test_user['id'])
    session.add(new_vote)
    session.commit()

def test_vote_a_post(authorized_client,create_test_posts):

    res = authorized_client.post(f"/vote/", json = 
    {
        "post_id":create_test_posts[0].id,
        "direction": 1
    })
    assert res.status_code == 201


def test_vote_a_post_unAuthUsewr(client,create_test_posts):

    res = client.post(f"/vote/", json = 
    {
        "post_id":create_test_posts[0].id,
        "direction": 1
    })
    assert res.json().get('detail') == "Not authenticated"
    assert res.status_code == 401



def test_vote_a_post_twice(authorized_client,create_test_posts,create_a_vote):

    res = authorized_client.post(f"/vote/", json = 
     {
         "post_id":create_test_posts[3].id,
        "direction": 1
    })
    assert res.status_code == 409


def test_remove_Vote_from_a_post_already_voted(authorized_client,create_test_posts,create_a_vote):
    res = authorized_client.post(f"/vote/", json = 
     {
         "post_id":create_test_posts[3].id,
        "direction": 0
    })
    assert res.status_code == 201



def test_remove_Vote_from_a_post_not_voted(authorized_client,create_test_posts):
    res = authorized_client.post(f"/vote/", json = 
     {
         "post_id":create_test_posts[0].id,
         "direction": 0
    })
    assert res.status_code == 404



def test__Vote_a_invalid_post(authorized_client,create_test_posts):
    res = authorized_client.post(f"/vote/", json = 
     {
         "post_id":0,
         "direction": 1
    })
    assert res.status_code == 404





