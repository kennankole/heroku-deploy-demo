from pydoc import cli


def test_home(client):
    assert client.get('/').status_code == 200
    
def test_school(client):
    assert client.get('/school').status_code == 200 
    
def test_upload_files(client):
    assert client.post('/articles').status_code == 200 
    
    
def test_school_home_page(client):
    assert client.get('/school/home').status_code == 200
    