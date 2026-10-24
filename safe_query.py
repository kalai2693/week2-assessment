
import psycopg2

def get_orders(customer_id):
    connection = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password='Kalaiarasan123'
    )

    try:
        cursor = connection.cursor()

        # Parameterized query prevents SQL injection
        query = """
            SELECT * FROM orders
            WHERE customer_id::text = %s
        """
        cursor.execute(query, (str(customer_id),))
        results = cursor.fetchall()

        print("Number of orders:", len(results))
        print(results)

    finally:
        connection.close()


get_orders("1 OR 1=1")
