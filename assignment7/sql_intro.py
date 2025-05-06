import sqlite3
from pathlib import Path

# Ensure database directory exists
Path("../db").mkdir(exist_ok=True)

# Database connection
db_path = "../db/magazines.db"

def add_publisher(cursor, name):
    """Add a publisher if it doesn't already exist."""
    try:
        cursor.execute("SELECT name FROM publishers WHERE name = ?", (name,))
        if cursor.fetchone():
            print(f"Publisher '{name}' already exists.")
            return False
        cursor.execute("INSERT INTO publishers (name) VALUES (?)", (name,))
        print(f"Added publisher '{name}'.")
        return True
    except sqlite3.Error as e:
        print(f"Error adding publisher '{name}': {e}")
        return False

def add_magazine(cursor, name, publisher_name):
    """Add a magazine if it doesn't already exist, linked to a publisher."""
    try:
        # Check if publisher exists
        cursor.execute("SELECT publisher_id FROM publishers WHERE name = ?", (publisher_name,))
        publisher = cursor.fetchone()
        if not publisher:
            print(f"Publisher '{publisher_name}' does not exist.")
            return False
        publisher_id = publisher[0]
        
        # Check if magazine exists
        cursor.execute("SELECT name FROM magazines WHERE name = ?", (name,))
        if cursor.fetchone():
            print(f"Magazine '{name}' already exists.")
            return False
            
        cursor.execute(
            "INSERT INTO magazines (name, publisher_id) VALUES (?, ?)",
            (name, publisher_id)
        )
        print(f"Added magazine '{name}' for publisher '{publisher_name}'.")
        return True
    except sqlite3.Error as e:
        print(f"Error adding magazine '{name}': {e}")
        return False

def add_subscriber(cursor, name, address):
    """Add a subscriber if the name-address pair doesn't already exist."""
    try:
        cursor.execute(
            "SELECT name, address FROM subscribers WHERE name = ? AND address = ?",
            (name, address)
        )
        if cursor.fetchone():
            print(f"Subscriber '{name}' at '{address}' already exists.")
            return False
        cursor.execute(
            "INSERT INTO subscribers (name, address) VALUES (?, ?)",
            (name, address)
        )
        print(f"Added subscriber '{name}' at '{address}'.")
        return True
    except sqlite3.Error as e:
        print(f"Error adding subscriber '{name}': {e}")
        return False

def add_subscription(cursor, subscriber_name, subscriber_address, magazine_name, expiration_date):
    """Add a subscription if it doesn't already exist."""
    try:
        # Check if subscriber exists
        cursor.execute(
            "SELECT subscriber_id FROM subscribers WHERE name = ? AND address = ?",
            (subscriber_name, subscriber_address)
        )
        subscriber = cursor.fetchone()
        if not subscriber:
            print(f"Subscriber '{subscriber_name}' at '{subscriber_address}' does not exist.")
            return False
        subscriber_id = subscriber[0]
        
        # Check if magazine exists
        cursor.execute("SELECT magazine_id FROM magazines WHERE name = ?", (magazine_name,))
        magazine = cursor.fetchone()
        if not magazine:
            print(f"Magazine '{magazine_name}' does not exist.")
            return False
        magazine_id = magazine[0]
        
        # Check if subscription exists
        cursor.execute(
            "SELECT subscriber_id, magazine_id FROM subscriptions WHERE subscriber_id = ? AND magazine_id = ?",
            (subscriber_id, magazine_id)
        )
        if cursor.fetchone():
            print(f"Subscription for '{subscriber_name}' to '{magazine_name}' already exists.")
            return False
            
        cursor.execute(
            "INSERT INTO subscriptions (subscriber_id, magazine_id, expiration_date) VALUES (?, ?, ?)",
            (subscriber_id, magazine_id, expiration_date)
        )
        print(f"Added subscription for '{subscriber_name}' to '{magazine_name}'.")
        return True
    except sqlite3.Error as e:
        print(f"Error adding subscription for '{subscriber_name}' to '{magazine_name}': {e}")
        return False

try:
    # Connect to database
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = 1")  # Enable foreign key constraints
    cursor = conn.cursor()

    # Create publishers table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS publishers (
            publisher_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    """)

    # Create magazines table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS magazines (
            magazine_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            publisher_id INTEGER NOT NULL,
            FOREIGN KEY (publisher_id) REFERENCES publishers(publisher_id)
        )
    """)

    # Create subscribers table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subscribers (
            subscriber_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            address TEXT NOT NULL
        )
    """)

    # Create subscriptions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subscriptions (
            subscription_id INTEGER PRIMARY KEY AUTOINCREMENT,
            subscriber_id INTEGER NOT NULL,
            magazine_id INTEGER NOT NULL,
            expiration_date TEXT NOT NULL,
            FOREIGN KEY (subscriber_id) REFERENCES subscribers(subscriber_id),
            FOREIGN KEY (magazine_id) REFERENCES magazines(magazine_id),
            UNIQUE (subscriber_id, magazine_id)
        )
    """)

    # Populate publishers
    add_publisher(cursor, "NewsCorp")
    add_publisher(cursor, "Time Inc")
    add_publisher(cursor, "Conde Nast")

    # Populate magazines
    add_magazine(cursor, "Tech Trends", "NewsCorp")
    add_magazine(cursor, "Fashion Weekly", "Conde Nast")
    add_magazine(cursor, "Health Digest", "Time Inc")

    # Populate subscribers
    add_subscriber(cursor, "John Doe", "123 Main St, Cityville")
    add_subscriber(cursor, "Jane Smith", "456 Oak Ave, Townsville")
    add_subscriber(cursor, "Alex Brown", "789 Pine Rd, Villageburg")

    # Populate subscriptions
    add_subscription(cursor, "John Doe", "123 Main St, Cityville", "Tech Trends", "2026-04-30")
    add_subscription(cursor, "Jane Smith", "456 Oak Ave, Townsville", "Fashion Weekly", "2025-12-31")
    add_subscription(cursor, "Alex Brown", "789 Pine Rd, Villageburg", "Health Digest", "2026-06-30")

    # Query 1: All subscribers
    print("\nAll Subscribers:")
    cursor.execute("SELECT * FROM subscribers")
    subscribers = cursor.fetchall()
    for row in subscribers:
        print(row)

    # Query 2: All magazines sorted by name
    print("\nAll Magazines (Sorted by Name):")
    cursor.execute("SELECT * FROM magazines ORDER BY name")
    magazines = cursor.fetchall()
    for row in magazines:
        print(row)

    # Query 3: Magazines for publisher 'NewsCorp' (using JOIN)
    print("\nMagazines by Publisher 'NewsCorp':")
    cursor.execute("""
        SELECT magazines.magazine_id, magazines.name, publishers.name AS publisher_name
        FROM magazines
        JOIN publishers ON magazines.publisher_id = publishers.publisher_id
        WHERE publishers.name = 'NewsCorp'
    """)
    publisher_magazines = cursor.fetchall()
    for row in publisher_magazines:
        print(row)

    # Commit changes
    conn.commit()

except sqlite3.Error as e:
    print(f"An error occurred: {e}")

finally:
    # Close connection
    if conn:
        conn.close()
        print("\nDatabase connection closed.")