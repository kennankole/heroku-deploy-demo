import io
from urllib import response
from app.models import Document
from unittest import mock
from flask import url_for
from app.tests.conftest import mock_my_model

def test_home(client):
    assert client.get('/').status_code == 200
    
def test_school(client):
    assert client.get('/school').status_code == 200 

def test_support_page(client):
    assert client.get('/support').status_code == 200
    
def test_list_documents(app_test):
    with app_test.test_client() as clients:
        response = clients.get('/documents')
        assert response.status_code == 200
    
   
    
def test_upload_files(client):
    assert client.post('/articles/1/').status_code == 200 
    data = {
        'title': 'Docker',
        'author': 'kennankole'
    }
    data = {key: str(value) for key, value in data.items()}
    data['file'] = (io.BytesIO(b"abcdef"), "test.jpeg")
    
    response = client.post(
        url_for('home.list_documents'), data=data, follow_redirects=True,
        content_type='multipart/form-data'
    )
    
    assert response.status_code == 201
    
def test_school_home_page(client):
    assert client.get('/school/home').status_code == 200
    