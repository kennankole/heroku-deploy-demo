def test_home(client):
    assert client.get('/').status_code == 200
    
def test_school(client):
    assert client.get('/school').status_code == 200 
    