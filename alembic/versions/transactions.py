from sqlalchemy.orm import Session
from sqlalchemy import select
from models import Customer, Order, Product
from database import engine


def place_order(customer_id: int, product_id: int, quantity: int, amount: float):
    if quantity <= 0:
        raise ValueError("Quantity must be greater than zero")

    with Session(engine) as session:
        try:
            with session.begin():
                product = session.get(Product, product_id)

                if product is None:
                    raise ValueError("Product not found")

                if product.stock < quantity:
                    raise ValueError("Insufficient stock")

                product.stock -= quantity

                order = Order(
                    customer_id=customer_id,
                    amount=amount
                )
                session.add(order)

            print("Order placed successfully!")

        except Exception as error:
            print("Order failed. Transaction rolled back:", error)
            raise


if __name__ == "__main__":
    place_order(
        customer_id=1,
        product_id=1,
        quantity=2,
        amount=1000.00
    )