def test_home(client):
    assert client.get('/home').status_code == 200
    
