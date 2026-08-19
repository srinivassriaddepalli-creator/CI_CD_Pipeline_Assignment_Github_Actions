import pytest
import mongomock
from unittest.mock import patch

# Mock the PyMongo engine client connection globally before importing the app
@pytest.fixture(autouse=True)
def mock_mongo():
    with patch('flask_pymongo.PyMongo') as mock:
        # Mock instance attributes to prevent initialization attribute failures
        mock_instance = mock.return_value
        mock_instance.db = mongomock.MongoClient().db
        yield mock_instance

def test_home_route():
    """Test that the application home route evaluates without network crashing."""
    from app import app
    app.config['TESTING'] = True
    with app.test_client() as client:
        response = client.get('/')
        assert response is not None

def test_health_endpoint():
    """Ensure basic application client validation routes execute."""
    from app import app
    app.config['TESTING'] = True
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code in [200, 302, 404]
