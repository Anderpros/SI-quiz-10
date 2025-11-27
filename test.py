# test.py
import pytest
from main import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "testkey"
    with app.test_client() as client:
        yield client

def test_read_main(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok", "version": "1.0.0"}

def test_addition_logic(client):
    response = client.get("/add/5/10")
    assert response.status_code == 200
    assert response.get_json() == {"result": 15}

def test_invalid_input(client):
    response = client.get("/add/five/ten")
    assert response.status_code == 404

def test_login_success(client):
    response = client.post("/login", json={
        "username": "leonard",
        "password": "12345"
    })
    assert response.status_code == 200
    assert response.get_json() == {"message": "Login success"}

def test_login_fail(client):
    response = client.post("/login", json={
        "username": "wrong",
        "password": "wrong"
    })
    assert response.status_code == 401
    assert response.get_json() == {"error": "Invalid credentials"}

def test_subtract_unauthorized(client):
    response = client.get("/subtract/10/5")
    assert response.status_code == 401
    assert response.get_json() == {"error": "Unauthorized"}

def test_subtract_authorized(client):
    # login first
    client.post("/login", json={
        "username": "admin",
        "password": "admin123"
    })

    # now call subtract
    response = client.get("/subtract/10/5")
    assert response.status_code == 200
    assert response.get_json() == {"result": 5}
