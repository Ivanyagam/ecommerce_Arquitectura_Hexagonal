import sqlite3

SCHEMA = """
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL, price REAL NOT NULL, stock INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT, customer_email TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS order_lines (
    order_id INTEGER NOT NULL, product_id INTEGER NOT NULL,
    product_name TEXT NOT NULL, unit_price REAL NOT NULL, quantity INTEGER NOT NULL
);
"""


def connect(path: str) -> sqlite3.Connection:
    connection = sqlite3.connect(path, check_same_thread=False)
    connection.row_factory = sqlite3.Row
    connection.executescript(SCHEMA)
    return connection
