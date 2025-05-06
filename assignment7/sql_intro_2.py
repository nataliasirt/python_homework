import sqlite3
import pandas as pd

# Database path
db_path = "../db/lesson.db"

try:
    # Connect to database
    conn = sqlite3.connect(db_path)

    # Query to join line_items and products
    query = """
        SELECT line_items.line_item_id, line_items.quantity, line_items.product_id,
               products.product_name, products.price
        FROM line_items
        JOIN products ON line_items.product_id = products.product_id
    """
    
    # Read data into DataFrame
    df = pd.read_sql_query(query, conn)
    
    # Print first 5 rows
    print("First 5 rows of initial DataFrame:")
    print(df.head())
    
    # Add total column (quantity * price)
    df['total'] = df['quantity'] * df['price']
    
    # Print first 5 rows with total column
    print("\nFirst 5 rows with total column:")
    print(df.head())
    
    # Group by product_id, aggregate line_item_id (count), total (sum), product_name (first)
    summary_df = df.groupby('product_id').agg({
        'line_item_id': 'count',
        'total': 'sum',
        'product_name': 'first'
    }).reset_index()
    
    # Rename columns for clarity
    summary_df.columns = ['product_id', 'order_count', 'total_price', 'product_name']
    
    # Print first 5 rows of grouped DataFrame
    print("\nFirst 5 rows of grouped DataFrame:")
    print(summary_df.head())
    
    # Sort by product_name
    summary_df = summary_df.sort_values('product_name')
    
    # Write to CSV
    summary_df.to_csv("order_summary.csv", index=False)
    print("\nDataFrame written to order_summary.csv")

except sqlite3.Error as e:
    print(f"Database error: {e}")
except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close connection
    if conn:
        conn.close()
        print("Database connection closed.")