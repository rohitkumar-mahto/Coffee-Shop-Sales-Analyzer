import numpy as np
import pandas as pd

# ==========================================
# 1. GENERATE MOCK DATA (The "Messy" Dataset)
# ==========================================
np.random.seed(42) # Ensures identical random numbers each run

num_transactions = 200
products = ['Espresso', 'Latte', 'Americano', 'Muffin', 'Croissant']
price_map = {'Espresso': 2.50, 'Latte': 4.00, 'Americano': 3.00, 'Muffin': 3.50, 'Croissant': 3.75}

transaction_id = np.arange(1, num_transactions + 1)
product_type = np.random.choice(products, size=num_transactions)
price_per_item = np.array([price_map[p] for p in product_type])
quantity_sold = np.random.randint(1, 5, size=num_transactions)

# Inject messy data (negative quantities and missing prices)
negative_indices = np.random.choice(num_transactions, size=5, replace=False)
quantity_sold[negative_indices] = -1

missing_price_indices = np.random.choice(num_transactions, size=10, replace=False)
price_per_item[missing_price_indices] = np.nan

day_of_month = np.random.randint(1, 31, size=num_transactions)

# Build the initial DataFrame
df = pd.DataFrame({
    'Transaction_ID': transaction_id,
    'Day': day_of_month,
    'Product': product_type,
    'Quantity': quantity_sold,
    'Price': price_per_item
}).sort_values(by='Day').reset_index(drop=True)

# ==========================================
# 2. CLEAN THE DATA
# ==========================================
# Remove negative/zero quantities
df_clean = df[df['Quantity'] > 0].copy()

# Fill missing prices with the mean price of that specific product
df_clean['Price'] = df_clean['Price'].fillna(
    df_clean.groupby('Product')['Price'].transform('mean')
)

# ==========================================
# 3. ANALYZE BUSINESS METRICS
# ==========================================
# Calculate Total Revenue per transaction
df_clean['Total_Revenue'] = df_clean['Quantity'] * df_clean['Price']

# Metric A: Best-Selling Item by Volume
volume_sales = df_clean.groupby('Product')['Quantity'].sum().sort_values(ascending=False)

# Metric B: Biggest Revenue Driver
revenue_sales = df_clean.groupby('Product')['Total_Revenue'].sum().sort_values(ascending=False)

# Metric C: Daily Sales Consistency (using NumPy to calculate standard deviation)
daily_revenue = df_clean.groupby('Day')['Total_Revenue'].sum()
revenue_std_dev = np.std(daily_revenue)
average_daily_revenue = np.mean(daily_revenue)

# ==========================================
# 4. PRINT RESULTS & EXPORT
# ==========================================
print("--- COFFEE SHOP SALES REPORT ---\n")

print("1. Best-Selling Items (Volume):")
print(volume_sales)

print("\n2. Biggest Revenue Drivers ($):")
print(revenue_sales)

print("\n3. Daily Revenue Stats:")
print(f"Average Daily Revenue: ${average_daily_revenue:.2f}")
print(f"Revenue Standard Deviation: ${revenue_std_dev:.2f}")
print(f"(A high standard deviation means sales fluctuate wildly day-to-day)")

# Export the clean dataset to a CSV file
df_clean.to_csv('coffee_shop_cleaned_data.csv', index=False)
print("\n[Success] Clean dataset exported to 'coffee_shop_cleaned_data.csv'")