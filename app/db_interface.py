import sqlite3
import logging

logging.basicConfig(level=logging.INFO)

class DBInterface:
    def __init__(self, db_path='carelite.db'):
        self.db_path = db_path

    def connect(self):
        return sqlite3.connect(self.db_path)

    def init_tables(self):
        conn = self.connect()
        cursor = conn.cursor()
        # Customers
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id TEXT UNIQUE,
                age INTEGER,
                gender TEXT,
                location TEXT,
                browsing_history TEXT,
                purchase_history TEXT,
                customer_segment TEXT,
                avg_order_value REAL,
                holiday TEXT,
                season TEXT
            )
        ''')
        # Products
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id TEXT UNIQUE,
                category TEXT,
                subcategory TEXT,
                price REAL,
                brand TEXT,
                avg_rating_similar REAL,
                product_rating REAL,
                customer_review_sentiment_score REAL,
                holiday TEXT,
                season TEXT,
                geographical_location TEXT,
                similar_product_list TEXT,
                probability_of_recommendation REAL
            )
        ''')
        # User activity
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_activity (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id TEXT,
                product_id TEXT,
                activity_type TEXT,
                activity_time DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        # Feedback
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id TEXT,
                product_id TEXT,
                clicked INTEGER,
                dwell_time REAL,
                feedback_time DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
        logging.info("Database tables initialized.")

    def insert_record(self, table, record):
        conn = self.connect()
        cursor = conn.cursor()
        cols = ", ".join(record.keys())
        placeholders = ", ".join("?" for _ in record)
        query = f"INSERT OR REPLACE INTO {table} ({cols}) VALUES ({placeholders})"
        cursor.execute(query, tuple(record.values()))
        conn.commit()
        conn.close()

    def fetch_query(self, query, params=None):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        rows = cursor.fetchall()
        conn.close()
        return rows

    def execute_query(self, query, params=None):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        conn.commit()
        conn.close()
