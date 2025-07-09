import pandas as pd
import json
import random
from faker import Faker
from datetime import datetime, timedelta
import uuid
import os

fake = Faker()
random.seed(42)

os.makedirs("data_sources", exist_ok=True)

# 1. Generate Products
categories = {
    'Electronics': ['Mobiles', 'Laptops', 'Headphones'],
    'Clothing': ['T-Shirts', 'Jeans', 'Jackets'],
    'Groceries': ['Fruits', 'Vegetables', 'Snacks'],
}

brands = ['Nike', 'Samsung', 'Apple', 'Puma', 'LG', 'Sony', 'Levi’s', 'AmazonBasics']
products = []

for i in range(1, 501):  # 500 products
    category = random.choice(list(categories.keys()))
    subcat = random.choice(categories[category])
    brand = random.choice(brands)
    cost = round(random.uniform(50, 5000), 2)
    retail = round(cost * random.uniform(1.1, 1.8), 2)
    products.append({
        'product_id': i,
        'name': f"{brand} {subcat} {i}",
        'category': category,
        'subcategory': subcat,
        'brand': brand,
        'cost_price': cost,
        'retail_price': retail,
        'is_active': random.choice([True, True, True, False])
    })

pd.DataFrame(products).to_csv("data_sources/products.csv", index=False)

# 2. Generate Stores
store_types = ['Flagship', 'Franchise', 'Express']
stores = []

for i in range(1, 31):  # 30 stores
    stores.append({
        'store_id': i,
        'name': f"{fake.company()} Store {i}",
        'location': fake.city(),
        'region': random.choice(['North', 'South', 'East', 'West']),
        'store_type': random.choice(store_types),
        'opened_date': fake.date_between(start_date='-5y', end_date='today').isoformat(),
        'is_active': random.choice([True, True, True, False])
    })

with open("data_sources/store_data.json", "w") as f:
    json.dump(stores, f, indent=2)

# 3. Generate Customers
customers = []

for i in range(1, 10001):  # 10,000 customers
    dob = fake.date_of_birth(minimum_age=18, maximum_age=70)
    customers.append({
        'customer_id': i,
        'name': fake.name(),
        'gender': random.choice(['M', 'F', 'Other']),
        'dob': dob.isoformat(),
        'email': fake.email(),
        'phone': fake.phone_number(),
        'signup_date': fake.date_between(start_date='-5y', end_date='today').isoformat(),
        'loyalty_points': random.randint(0, 1000),
        'is_active': random.choice([True, True, True, False])
    })

pd.DataFrame(customers).to_csv("data_sources/customers.csv", index=False)

# 4. Generate Sales
sales = []
start_date = datetime.now() - timedelta(days=365)
payment_methods = ['Cash', 'Card', 'UPI', 'Wallet']
sales_channels = ['In-Store', 'Online']
promotion_codes = ['SAVE10', 'BOGO', 'FREESHIP', None, None]

for _ in range(100000):  # 100,000 sales
    timestamp = start_date + timedelta(minutes=random.randint(0, 525600))
    product = random.choice(products)
    quantity = random.randint(1, 5)
    unit_price = product['retail_price']
    discount = round(random.uniform(0, 0.3), 2)  # Up to 30%
    total = round(quantity * unit_price * (1 - discount), 2)

    sales.append({
        'sale_id': str(uuid.uuid4()),
        'timestamp': timestamp.isoformat(),
        'store_id': random.randint(1, 30),
        'product_id': product['product_id'],
        'customer_id': random.randint(1, 10000),
        'quantity': quantity,
        'unit_price': unit_price,
        'total_amount': total,
        'discount_applied': discount,
        'payment_method': random.choice(payment_methods),
        'is_refunded': random.choice([False]*95 + [True]*5),
        'sales_channel': random.choice(sales_channels),
        'promotion_code': random.choice(promotion_codes)
    })

pd.DataFrame(sales).to_csv("data_sources/sales_data.csv", index=False)

print(" Data generation complete.")
