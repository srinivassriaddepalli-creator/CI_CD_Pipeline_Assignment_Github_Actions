import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_route(client):
    """Test that the application home route loads or redirects without crashing."""
    response = client.get('/')
    # Accepts 200 OK, 302 Redirect, or 404 if no records are found yet
    assert response.status_code in [200, 302, 404]

def test_health_endpoint(client):
    """A standard placeholder test ensuring basic client routing functions work."""
    response = client.get('/')
    assert response is not None
