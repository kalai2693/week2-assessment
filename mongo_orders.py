from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client["week2_assessment"]
orders = db["order_events"]

# Clear previous test data
orders.delete_many({})

# Insert 5 order events
events = [
    {"customer_id": 1, "amount": 1000},
    {"customer_id": 2, "amount": 500},
    {"customer_id": 1, "amount": 700},
    {"customer_id": 3, "amount": 300},
    {"customer_id": 2, "amount": 800},
]

orders.insert_many(events)
print("5 order events inserted successfully!")

# Calculate total amount for each customer
pipeline = [
    {
        "$group": {
            "_id": "$customer_id",
            "total_amount": {"$sum": "$amount"}
        }
    },
    {"$sort": {"_id": 1}}
]

for result in orders.aggregate(pipeline):
    print(result)

client.close()