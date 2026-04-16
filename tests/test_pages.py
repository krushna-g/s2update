import pytest
from S2Digital import create_app
from S2Digital.extensions import db
from S2Digital.models import Contact
import json

@pytest.fixture
def app():
    app = create_app("S2Digital.config.TestConfig")
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_pages_get(client):
    routes = ["/", "/about", "/products", "/services", "/contact"]
    for r in routes:
        rv = client.get(r)
        assert rv.status_code == 200

def test_contact_submit_valid(client, app):
    payload = {"name": "Alice", "email": "alice@example.com", "message": "Hello"}
    rv = client.post("/contact/submit", json=payload)
    assert rv.status_code == 201
    data = rv.get_json()
    assert data.get("ok") is True
    # check saved in DB
    with app.app_context():
        assert Contact.query.count() == 1
        c = Contact.query.first()
        assert c.name == "Alice"
        assert c.email == "alice@example.com"

def test_contact_submit_invalid(client):
    # missing fields
    rv = client.post("/contact/submit", json={"name": "", "email": "", "message": ""})
    assert rv.status_code == 400

def test_contact_xss_escaped(client, app):
    # submit message with script tag
    payload = {"name": "Bob", "email": "bob@example.com", "message": "<script>alert(1)</script>"}
    rv = client.post("/contact/submit", json=payload)
    assert rv.status_code == 201
    # access admin page with default key 'changeme'
    rv = client.get("/admin?key=changeme")
    assert rv.status_code == 200
    body = rv.data.decode("utf-8")
    # admin template should escape script tag (render &lt;script&gt;)
    assert "&lt;script&gt;" in body
    assert "<script>alert(1)</script>" not in body

def test_chat_api(client):
    rv = client.post("/api/chat", json={"message": "hello"})
    assert rv.status_code == 200
    data = rv.get_json()
    assert data.get("ok") is True
    assert "Echo:" in data.get("reply", "")