import pandas as pd

print("Loading datasets...")
customers = pd.read_csv('olist_customers_dataset.csv')
orders = pd.read_csv('olist_orders_dataset.csv')
order_items = pd.read_csv('olist_order_items_dataset.csv')
products = pd.read_csv('olist_products_dataset.csv')

print("Datasets loaded successfully!")
print(f"Customers shape: {customers.shape}")
print(f"Orders shape: {orders.shape}")
print(f"Order Items shape: {order_items.shape}")

# Convert date columns to proper datetime format
orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
orders['order_approved_at'] = pd.to_datetime(orders['order_approved_at'])
orders['order_delivered_customer_date'] = pd.to_datetime(orders['order_delivered_customer_date'])

# Drop rows with missing prices or freight values
order_items = order_items.dropna(subset=['price', 'freight_value'])

# Merge datasets into a master clean dataframe
print("Merging datasets...")
master_df = orders.merge(order_items, on='order_id', how='inner') \
                  .merge(customers, on='customer_id', how='left') \
                  .merge(products, on='product_id', how='left')

print(f"Master clean dataset shape: {master_df.shape}")

# Save the clean master file for your database / Power BI
master_df.to_csv('ecommerce_master_clean.csv', index=False)
print("Clean dataset saved successfully as 'ecommerce_master_clean.csv'!")