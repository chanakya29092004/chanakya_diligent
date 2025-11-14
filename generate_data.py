import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

random.seed(42)

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

countries = ['USA', 'Canada', 'UK', 'Germany', 'France', 'Australia', 'India', 'Japan']

users = []
start_date = datetime(2021, 1, 1)
for i in range(1, 101):
    created = start_date + timedelta(days=random.randint(0, 1400))
    users.append({
        'user_id': i,
        'name': f"User {i}",
        'email': f"user{i}@example.com",
        'created_at': created.strftime('%Y-%m-%d %H:%M:%S'),
        'country': random.choice(countries)
    })

with open(DATA_DIR / "users.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=['user_id','name','email','created_at','country'])
    writer.writeheader()
    writer.writerows(users)

categories = ['Electronics','Home','Fashion','Beauty','Sports','Toys','Books','Groceries']
products = []
for i in range(1, 121):
    products.append({
        'product_id': i,
        'product_name': f"Product {i}",
        'category': random.choice(categories),
        'price': f"{random.uniform(5, 500):.2f}",
        'stock': random.randint(10, 500)
    })

with open(DATA_DIR / "products.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=['product_id','product_name','category','price','stock'])
    writer.writeheader()
    writer.writerows(products)

orders = []
for i in range(1, 161):
    user = random.choice(users)
    order_date = datetime(2022,1,1) + timedelta(days=random.randint(0, 1000))
    total = round(random.uniform(20, 2000),2)
    status = random.choice(['paid','pending','refunded'])
    orders.append({
        'order_id': i,
        'user_id': user['user_id'],
        'order_date': order_date.strftime('%Y-%m-%d %H:%M:%S'),
        'total_amount': f"{total:.2f}",
        'payment_status': status
    })

with open(DATA_DIR / "orders.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=['order_id','user_id','order_date','total_amount','payment_status'])
    writer.writeheader()
    writer.writerows(orders)

order_items = []
item_id = 1
for order in orders:
    for _ in range(random.randint(1,4)):
        product = random.choice(products)
        quantity = random.randint(1,5)
        line_total = quantity * float(product['price'])
        order_items.append({
            'item_id': item_id,
            'order_id': order['order_id'],
            'product_id': product['product_id'],
            'quantity': quantity,
            'line_total': f"{line_total:.2f}"
        })
        item_id +=1

with open(DATA_DIR / "order_items.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=['item_id','order_id','product_id','quantity','line_total'])
    writer.writeheader()
    writer.writerows(order_items)

reviews = []
for i in range(1, 51):
    user = random.choice(users)
    product = random.choice(products)
    created = datetime(2022,6,1) + timedelta(days=random.randint(0, 900))
    reviews.append({
        'review_id': i,
        'user_id': user['user_id'],
        'product_id': product['product_id'],
        'rating': random.randint(1,5),
        'review_text': random.choice([
            'Great quality and fast shipping.',
            'Product matches the description.',
            'Satisfied with the purchase.',
            'Could be better, but decent value.',
            'Exceeded my expectations!',
            'Not satisfied with the durability.',
            'Amazing customer support with this order.',
            'Packaging was secure and neat.',
            'Would recommend to friends.',
            'Arrived earlier than expected.'
        ]),
        'created_at': created.strftime('%Y-%m-%d %H:%M:%S')
    })

with open(DATA_DIR / "reviews.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=['review_id','user_id','product_id','rating','review_text','created_at'])
    writer.writeheader()
    writer.writerows(reviews)
