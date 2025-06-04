import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

conn = sqlite3.connect('../db/lesson.db')

query = """
SELECT o.order_id, SUM(p.price * l.quantity) AS total_price
FROM orders o
JOIN line_items l ON o.order_id = l.order_id
JOIN products p ON l.product_id = p.product_id
GROUP BY o.order_id
"""

df = pd.read_sql_query(query, conn)

conn.close()

df['cumulative'] = df['total_price'].cumsum()

plt.figure(figsize=(10, 6))
df.plot(kind='line', x='order_id', y='cumulative', color='navy')

plt.title('Cumulative Revenue by Order ID')
plt.xlabel('Order ID')
plt.ylabel('Cumulative Revenue ($)')
plt.grid(True, linestyle='--', alpha=0.7)

plt.savefig('cumulative_revenue.png')