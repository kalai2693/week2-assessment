
import hashlib
import hmac

from fastapi.testclient import TestClient
from main import app, customers, API_KEY, WEBHOOK_SECRET

client = TestClient(app)


def setup_function():
    customers.clear()


def test_home():
    response = client.get("/")
    assert response.status_code == 200


def test_create_customer_with_api_key():
    response = client.post(
        "/customers",
        headers={"x-api-key": API_KEY},
        json={"id": 1, "name": "Arun", "email": "arun@example.com"},
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Arun"


def test_create_customer_without_api_key():
    response = client.post(
        "/customers",
        json={"id": 1, "name": "Arun", "email": "arun@example.com"},
    )
    assert response.status_code == 401


def test_list_customers():
    customers[1] = {"id": 1, "name": "Arun", "email": "arun@example.com"}
    response = client.get("/customers")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_customer():
    client.post(
        "/customers",
        headers={"x-api-key": API_KEY},
        json={"id": 1, "name": "Arun", "email": "arun@example.com"},
    )
    response = client.get("/customers/1")
    assert response.status_code == 200


def test_missing_customer():
    response = client.get("/customers/999")
    assert response.status_code == 404


def test_update_customer():
    client.post(
        "/customers",
        headers={"x-api-key": API_KEY},
        json={"id": 1, "name": "Arun", "email": "arun@example.com"},
    )
    response = client.put(
        "/customers/1",
        json={"id": 1, "name": "Arun Updated", "email": "updated@example.com"},
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Arun Updated"


def test_delete_customer():
    client.post(
        "/customers",
        headers={"x-api-key": API_KEY},
        json={"id": 1, "name": "Arun", "email": "arun@example.com"},
    )
    response = client.delete("/customers/1")
    assert response.status_code == 200
    assert client.get("/customers/1").status_code == 404


def test_webhook_rejects_invalid_signature():
    response = client.post(
        "/webhook",
        json={"event": "order_created", "order_id": 101},
        headers={"x-signature": "wrong-signature"},
    )
    assert response.status_code == 401


def test_webhook_accepts_valid_signature():
    body = b'{"event":"order_created","order_id":101}'
    signature = hmac.new(
        WEBHOOK_SECRET.encode(),
        body,
        hashlib.sha256,
    ).hexdigest()

    response = client.post(
        "/webhook",
        content=body,
        headers={
            "x-signature": f"sha256={signature}",
            "content-type": "application/json",
        },
    )
    assert response.status_code == 200
