"""raw database operations"""

from dataclasses import asdict
import sqlite3
from domain import models


class Database:
    # when the db class is initialized, open db connection
    def __init__(self):
        # db file name
        file = "grocery_price_tracker.db"

        # connect to db
        self.connection = None

        try:
            self.connection = sqlite3.connect(file)
            print("connected to db")

            # create tables
            self.create_tables()

        except sqlite3.Error as e:
            print(f"Error: {e}")

    # create tables
    def create_tables(self):
        try:
            # sql table creation statements
            sql_statements = [
                """CREATE TABLE IF NOT EXISTS grocery_items (
                    item_id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL
                )
                """,
                """CREATE TABLE IF NOT EXISTS products (
                    product_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    brand TEXT,
                    size TEXT,
                    regular_price REAL,
                    promo_price REAL
                )
                """,
                """CREATE TABLE IF NOT EXISTS tracked_products (
                    tracked_product_id INTEGER PRIMARY KEY,
                    product_id TEXT NOT NULL,
                    item_id INTEGER NOT NULL,
                    is_active INTEGER NOT NULL DEFAULT 1,
                    FOREIGN KEY (product_id) REFERENCES products (product_id),
                    FOREIGN KEY (item_id) REFERENCES grocery_items (item_id),
                    UNIQUE(item_id, product_id)
                )
                """,
                """CREATE TABLE IF NOT EXISTS price_history (
                    price_history_id INTEGER PRIMARY KEY,
                    product_id TEXT NOT NULL,
                    captured_at TIMESTAMP NOT NULL,
                    regular_price REAL,
                    promo_price REAL,
                    FOREIGN KEY (product_id) REFERENCES products (product_id)
                )
                """,
            ]

            # create a cursor
            cursor = self.connection.cursor()

            # execute creation statements
            for statement in sql_statements:
                cursor.execute(statement)

            # commit the changes
            self.connection.commit()

            print("db tables created successfully")

        except sqlite3.Error as e:
            print(f"Error: {e}")

    # check if db is open
    def is_open(self):
        return self.connection != None

    # close db
    def closeDB(self):
        db_conn = self.connection

        if db_conn:
            db_conn.close()
            print("closed database")

    # insert grocery item
    def insert_grocery_item(self, name: str):
        sql_statement = """
        INSERT INTO grocery_items (name) 
        VALUES (:name)
        """
        try:
            # create cursor
            cursor = self.connection.cursor()

            # execute insert statement
            cursor.execute(sql_statement, asdict(models.GroceryItem(name=name)))

            # commit
            self.connection.commit()

            # return id
            return cursor.lastrowid

        except sqlite3.Error as e:
            print(f"Error: {e}")

    def get_grocery_items(self):
        sql_statement = """
        SELECT * FROM grocery_items
        """

        try:

            # create cursor
            cursor = self.connection.cursor()

            # execute sql
            cursor.execute(sql_statement)

            # get rows
            rows = cursor.fetchall()

            return rows
        except sqlite3.Error as e:
            print(f"Error: {e}")

    def delete_grocery_item(self, item_id):
        sql_statement = "DELETE FROM grocery_items WHERE item_id = ?"

        try:
            # create cursor
            cursor = self.connection.cursor()

            # execute sql
            cursor.execute(sql_statement, (item_id,))

            # commit changes
            self.connection.commit()

        except sqlite3.Error as e:
            print(f"Error: {e}")
            
    def insert_product(self, product):
        sql_statement = """
        INSERT INTO products (
            product_id, name, brand, size, regular_price, promo_price
        )
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(product_id)
        DO UPDATE SET
            name = excluded.name,
            brand = excluded.brand,
            size = excluded.size,
            regular_price = excluded.regular_price,
            promo_price = excluded.promo_price
        """

        try:
            cursor = self.connection.cursor()
            cursor.execute(
                sql_statement,
                (
                    product.product_id,
                    product.name,
                    product.brand,
                    product.size,
                    product.regular_price,
                    product.promo_price,
                ),
            )
            self.connection.commit()
        except Exception as e:
            print(f"Error: {e}")


    def insert_tracked_product(self, item_id: int, product_id: str):
        sql_statement = """
        INSERT INTO tracked_products (item_id, product_id, is_active)
        VALUES (?, ?, 1)
        ON CONFLICT(item_id, product_id)
        DO UPDATE SET is_active = 1
        """

        try:
            cursor = self.connection.cursor()
            cursor.execute(sql_statement, (item_id, product_id))
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error: {e}")
            
    def get_tracked_products_for_item(self, item_id: int):
        sql_statement = """
        SELECT 
            tp.tracked_product_id,
            p.product_id,
            p.name,
            p.brand,
            p.size,
            p.regular_price,
            p.promo_price
        FROM tracked_products tp
        JOIN products p ON tp.product_id = p.product_id
        WHERE tp.item_id = ? AND tp.is_active = 1
        """

        try:
            cursor = self.connection.cursor()
            cursor.execute(sql_statement, (item_id,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error: {e}")
            return []
        
    def remove_tracked_product(self, tracked_product_id: int):
        sql_statement = """
        UPDATE tracked_products
        SET is_active = 0
        WHERE tracked_product_id = ?
        """

        try:
            cursor = self.connection.cursor()
            cursor.execute(sql_statement, (tracked_product_id,))
            self.connection.commit()
        except Exception as e:
            print(f"Error: {e}")
