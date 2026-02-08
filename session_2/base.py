import sqlite3
# you will need to pip install pandas matplotlib
import pandas as pd
import matplotlib as mpl

def get_connection(db_path="orders.db"):
    """
    Establish a connection to the SQLite database.
    Returns a connection object.
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    return conn

def main():

    db = get_connection()
    

    db.close()


if __name__=="__main__":
    main()

def list_categories():
    query = """SELECT category FROM products"""

    db = get_connection()
    cursor = db.cursor()

    cursor.execute(query)
    results = cursor.fetchall()

    db.close()

    # Convert rows to normal Python list
    categories = [row["category"] for row in results]
    return categories

def customer_count():
    query = """SELECT COUNT(first_name) FROM customers"""

    db = get_connection()
    cursor = db.cursor()

    cursor.execute(query)
    results = cursor.fetchall()

    db.close()
    count = results[0][0]
    return count
    
def order_customer(customer_email):
    query ="""SELECT o.order_id,
    o.customer_id,
    o.order_date,
    o.status,
    o.total_amount
    FROM orders o
    JOIN customers c ON c.customer_id = o.customer_id
    WHERE c.email = ? """

    db = get_connection()
    cursor = db.cursor()

    cursor.execute(query,(customer_email,))
    results = cursor.fetchall()

    db.close()
    categories = [[row["order_id"], row["order_date"], row["status"], row["total_amount"]] for row in results]

    return categories

def product_under_2():
    query ="""SELECT product_id,name,category,price FROM products WHERE price<2; """

    db = get_connection()
    cursor = db.cursor()

    cursor.execute(query)
    results = cursor.fetchall()

    db.close()

    categories = [[row["product_id"], row["name"], row["category"], row["price"]] for row in results]
    return categories

def total_spent():
    query ="""SELECT c.customer_id, c.first_name,
    SUM(oi.unit_price*oi.quantity) AS total_spent
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    JOIN order_items oi ON o.order_id = oi.order_id
    GROUP BY c.customer_id, c.first_name
    ORDER BY total_spent DESC 
    LIMIT 5"""

    db = get_connection()
    cursor = db.cursor()

    cursor.execute(query)
    results = cursor.fetchall()

    db.close()
    categories = [[row["customer_id"], row["first_name"]] for row in results]
    return(categories)

def orders_per_category():
    query ="""SELECT p.category, COUNT(o.order_id) AS total_orders
    FROM orders o
    JOIN order_items oi ON o.order_id=oi.order_id
    JOIN products p ON oi.product_id=p.product_id
    GROUP BY p.category
    ORDER BY total_orders DESC
    """

    db = get_connection()
    cursor = db.cursor()

    cursor.execute(query)
    results = cursor.fetchall()

    db.close()

    categories = [[row["category"], row["total_orders"]] for row in results]
    return categories

def avg_products_order():
    query ="""SELECT AVG(quantity) FROM order_items"""

    db = get_connection()
    cursor = db.cursor()

    cursor.execute(query)
    results = cursor.fetchall()

    db.close()
    count = results[0][0]
    print(count)

avg_products_order()