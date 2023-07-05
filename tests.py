import pytest
from app import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_load_data_endpoint(client):
    response = client.get('/load-data')
    assert response.status_code == 200
    assert response.get_data(as_text=True) == 'Data loaded into database successfully'


def test_export_data(client):
    response = client.get('/export-data')
    assert response.status_code == 200
    assert response.mimetype == 'text/csv'
    assert 'attachment' in response.headers['Content-Disposition']
