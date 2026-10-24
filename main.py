import hashlib
import hmac
from fastapi import Request
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
import secrets

app = FastAPI(title="Week 2 Assessment API")
API_KEY = "week2-test-key"


class Customer(BaseModel):
    id: int
    name: str
    email: str


customers = {}


@app.get("/")
def home():
    return {"message": "Week 2 Assessment API is running"}


@app.post("/customers")
def create_customer(
    customer: Customer,
    x_api_key: str = Header(default="")
):
    if not secrets.compare_digest(x_api_key, API_KEY):
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key"
        )

    if customer.id in customers:
        raise HTTPException(
            status_code=409,
            detail="Customer already exists"
        )

    customers[customer.id] = customer
    return customer
    if customer.id in customers:
        raise HTTPException(status_code=409, detail="Customer already exists")

    customers[customer.id] = customer
    return customer


@app.get("/customers")
def get_customers(limit: int = 10, offset: int = 0):
    if limit < 1 or offset < 0:
        raise HTTPException(
            status_code=400,
            detail="limit must be positive and offset cannot be negative"
        )

    customer_list = list(customers.values())
    return customer_list[offset:offset + limit]


@app.get("/customers/{customer_id}")
def get_customer(customer_id: int):
    customer = customers.get(customer_id)

    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    return customer


@app.put("/customers/{customer_id}")
def update_customer(customer_id: int, customer: Customer):
    if customer_id not in customers:
        raise HTTPException(status_code=404, detail="Customer not found")

    if customer.id != customer_id:
        raise HTTPException(status_code=400, detail="Customer ID mismatch")

    customers[customer_id] = customer
    return customer


@app.delete("/customers/{customer_id}")
def delete_customer(customer_id: int):
    if customer_id not in customers:
        raise HTTPException(status_code=404, detail="Customer not found")

    del customers[customer_id]
    return {"message": "Customer deleted successfully"}
WEBHOOK_SECRET = "week2-webhook-secret"


@app.post("/webhook")
async def receive_webhook(
    request: Request,
    x_signature: str = Header(default="")
):
    body = await request.body()

    expected_signature = hmac.new(
        WEBHOOK_SECRET.encode(),
        body,
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(
        x_signature,
        f"sha256={expected_signature}"
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid webhook signature"
        )

    return {"message": "Webhook signature verified successfully"}