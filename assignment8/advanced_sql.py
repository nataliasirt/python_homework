import sqlite3
conn = sqlite3.connect('../db/lesson.db')
cursor = conn.cursor()

# Task 1: Complex JOINs with Aggregation
print("Task 1: Total price for first 5 orders")
cursor.execute("""
    SELECT o.order_id, SUM(p.price * li.quantity) as total_price
    FROM orders o
    JOIN line_items li ON o.order_id = li.order_id
    JOIN products p ON li.product_id = p.product_id
    GROUP BY o.order_id
    ORDER BY o.order_id
    LIMIT 5
""")
results = cursor.fetchall()
for row in results:
    print(row)

# Task 2: Understanding Subqueries
print("\nTask 2: Average order price per customer")
cursor.execute("""
    SELECT c.customer_name, AVG(sub.total_price) as average_total_price
    FROM customers c
    LEFT JOIN (
        SELECT o.customer_id as customer_id_b, SUM(p.price * li.quantity) as total_price
        FROM orders o
        JOIN line_items li ON o.order_id = li.order_id
        JOIN products p ON li.product_id = p.product_id
        GROUP BY o.order_id
    ) sub ON c.customer_id = sub.customer_id_b
    GROUP BY c.customer_id, c.customer_name
""")
results = cursor.fetchall()
for row in results:
    print(row)

# Task 3: Insert Transaction Based on Data
print("\nTask 3: Creating new order")
try:
    # Get customer_id for Perez and Sons
    cursor.execute("SELECT customer_id FROM customers WHERE customer_name = 'Perez and Sons'")
    customer_id = cursor.fetchone()
    if not customer_id:
        raise ValueError("Customer 'Perez and Sons' not found")
    customer_id = customer_id[0]

    # Get employee_id for Miranda Harris
    cursor.execute("SELECT employee_id FROM employees WHERE first_name = 'Miranda' AND last_name = 'Harris'")
    employee_id = cursor.fetchone()
    if not employee_id:
        raise ValueError("Employee 'Miranda Harris' not found")
    employee_id = employee_id[0]

    # Get 5 cheapest products
    cursor.execute("SELECT product_id FROM products ORDER BY price ASC LIMIT 5")
    product_ids = [row[0] for row in cursor.fetchall()]
    if len(product_ids) < 5:
        raise ValueError("Fewer than 5 products found")

    # Insert order
    cursor.execute("INSERT INTO orders (customer_id, employee_id, date) VALUES (?, ?, date('now'))",
                  (customer_id, employee_id))
    order_id = cursor.lastrowid

    # Insert & print line items
    for product_id in product_ids:
        cursor.execute("INSERT INTO line_items (order_id, product_id, quantity) VALUES (?, ?, 10)",
                      (order_id, product_id))
    cursor.execute("""
        SELECT li.line_item_id, li.quantity, p.product_name
        FROM line_items li
        JOIN products p ON li.product_id = p.product_id
        WHERE li.order_id = ?
    """, (order_id,))
    results = cursor.fetchall()
    for row in results:
        print(row)

    # Clean up
    cursor.execute("DELETE FROM line_items WHERE order_id = ?", (order_id,))
    cursor.execute("DELETE FROM orders WHERE order_id = ?", (order_id,))
    conn.commit()
except Exception as e:
    print(f"Task 3 Error: {e}")

# Task 4: Aggregation with HAVING
print("\nTask 4: Employees with more than 5 orders")
cursor.execute("""
    SELECT e.employee_id, e.first_name, e.last_name, COUNT(o.order_id) as order_count
    FROM employees e
    JOIN orders o ON e.employee_id = o.employee_id
    GROUP BY e.employee_id, e.first_name, e.last_name
    HAVING COUNT(o.order_id) > 5
""")
results = cursor.fetchall()
for row in results:
    print(row)

conn.close()