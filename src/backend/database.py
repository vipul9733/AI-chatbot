import sqlite3
import json
from datetime import datetime

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('restaurant.db', check_same_thread=False)
        self.create_tables()
        self.initialize_menu()

    def create_tables(self):
        # Create orders table
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT NOT NULL,
                items TEXT NOT NULL,
                total_amount REAL NOT NULL,
                order_status TEXT DEFAULT 'pending',
                order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Create menu table
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS menu (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_name TEXT NOT NULL,
                description TEXT,
                price REAL NOT NULL,
                category TEXT NOT NULL
            )
        ''')
        
        self.conn.commit()

    def initialize_menu(self):
        # Check if menu is already initialized
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM menu")
        if cursor.fetchone()[0] == 0:
            # Initial menu items
            menu_items = [
                ("Margherita Pizza", "Fresh tomato sauce, mozzarella, and basil", 12.99, "Pizza"),
                ("Pepperoni Pizza", "Classic pepperoni with cheese", 14.99, "Pizza"),
                ("Caesar Salad", "Romaine lettuce, croutons, parmesan", 8.99, "Salad"),
                ("Chocolate Cake", "Rich chocolate layer cake", 6.99, "Dessert"),
                ("Coca Cola", "330ml", 2.99, "Beverages")
            ]
            
            cursor.executemany(
                "INSERT INTO menu (item_name, description, price, category) VALUES (?, ?, ?, ?)",
                menu_items
            )
            self.conn.commit()

    def get_menu(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM menu")
        columns = [description[0] for description in cursor.description]
        menu_items = []
        for row in cursor.fetchall():
            menu_items.append(dict(zip(columns, row)))
        return menu_items

    def place_order(self, customer_name, items):
        try:
            items_json = json.dumps(items)
            total_amount = sum(item['price'] * item['quantity'] for item in items)
            
            cursor = self.conn.cursor()
            cursor.execute(
                """
                INSERT INTO orders (customer_name, items, total_amount)
                VALUES (?, ?, ?)
                """,
                (customer_name, items_json, total_amount)
            )
            self.conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error placing order: {e}")
            return None

    def get_order(self, order_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
        columns = [description[0] for description in cursor.description]
        row = cursor.fetchone()
        if row:
            return dict(zip(columns, row))
        return None