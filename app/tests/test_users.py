import pytest
from app.models import User 



@pytest.fixture(scope='module')
def creating_new_user():
    user = User("qwerty123", "ankole", "anko@bol.com","avatar.jpg")
    return user 

def test_new_user(creating_new_user, client):
    assert creating_new_user.unique_id == "qwerty123"
    assert creating_new_user.email == "anko@bol.com"
    assert creating_new_user.username == "ankole"
    assert creating_new_user.profile_pic == "avatar.jpg"
  
        
    
def test_login_page(client):
    assert client.post('/login').status_code == 302
    assert client.get('/').status_code == 200
    
   
def test_login_index_page(client):
    assert client.get('/').status_code == 200

def test_user_account(client):
    assert client.get('/account').status_code == 200

def test_logout_redirect(client):
    assert client.get('/logout', follow_redirects=True).status_code == 200