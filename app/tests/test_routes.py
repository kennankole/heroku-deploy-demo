
from pydoc import doc
from app.models import Document
from unittest import mock

from app.tests.conftest import mock_my_model

def test_home(client):
    assert client.get('/').status_code == 200
    
def test_school(client):
    assert client.get('/school').status_code == 200 

def test_support_page(client):
    assert client.get('/support').status_code == 200
    
def test_list_documents(mock_my_model, mock_get_sqlalchemy, client):
    mock_get_sqlalchemy.all.return_value = [mock_my_model]
    response = client.get('/documents/')
    assert response == [mock_my_model]
    assert response.status_code == 200
   
    
def test_upload_files(client):
    assert client.post('/articles/1/').status_code == 200 
    
    
def test_school_home_page(client):
    assert client.get('/school/home').status_code == 200
    