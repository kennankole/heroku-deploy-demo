def test_home(client):
    response = client.get('/home')
    assert b"Hello there!" in response.data