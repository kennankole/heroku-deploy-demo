import pytest
from app import create_app, db
import os 
import tempfile

from app.models import Document


@pytest.fixture()
def app():
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///memory:"
        }
    )
    yield app 
    

@pytest.fixture()
def client(app):
    return app.test_client()





@pytest.fixture
def db_handle():
    app = create_app()
    db_fd, db_fname = tempfile.mkstemp()
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + db_fname
    app.config['TESTING'] = True
    
    with app.test_client() as db_client:
        with app.app_context():
            db.create_all()
        yield db_client
    
    db.session.remove()
    os.close(db_fd)
    os.unlink(db_fname)
    
    

@pytest.fixture
def mock_my_model():
    my_model = Document(
        id="my_mock_id"
    )
    return my_model


@pytest.fixture
def mock_get_sqlalchemy(mocker):
    mock = mocker.patch("flask_sqlalchemy._QueryProperty.__get__").retun_value = mocker.Mock()
    return mock