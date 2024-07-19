from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# Cấu hình kết nối PostgreSQL
app.config['POSTGRES_USER'] = 'your_user'
app.config['POSTGRES_PASSWORD'] = 'your_password'
app.config['POSTGRES_DB'] = 'crm'
app.config['POSTGRES_HOST'] = 'localhost'
app.config['POSTGRES_PORT'] = '5432'

def get_db_connection():
    conn = psycopg2.connect(
        host=app.config['POSTGRES_HOST'],
        database=app.config['POSTGRES_DB'],
        user=app.config['POSTGRES_USER'],
        password=app.config['POSTGRES_PASSWORD']
    )
    return conn

@app.route('/customers', methods=['GET', 'POST'])
def manage_customers():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    if request.method == 'POST':
        data = request.json
        name = data['name']
        email = data['email']
        phone = data['phone']
        address = data['address']
        
        cursor.execute("INSERT INTO customers (name, email, phone, address) VALUES (%s, %s, %s, %s) RETURNING id", (name, email, phone, address))
        conn.commit()
        customer_id = cursor.fetchone()['id']
        cursor.close()
        conn.close()
        
        return jsonify({"message": "Customer added", "customer_id": customer_id}), 201

    cursor.execute("SELECT * FROM customers")
    customers = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return jsonify(customers)

@app.route('/products', methods=['GET', 'POST'])
def manage_products():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    if request.method == 'POST':
        data = request.json
        name = data['name']
        price = data['price']
        stock = data['stock']
        
        cursor.execute("INSERT INTO products (name, price, stock) VALUES (%s, %s, %s) RETURNING id", (name, price, stock))
        conn.commit()
        product_id = cursor.fetchone()['id']
        cursor.close()
        conn.close()
        
        return jsonify({"message": "Product added", "product_id": product_id}), 201

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return jsonify(products)

@app.route('/orders', methods=['GET', 'POST'])
def manage_orders():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    if request.method == 'POST':
        data = request.json
        customer_id = data['customer_id']
        order_date = data['order_date']
        total = data['total']
        items = data['items']
        
        cursor.execute("INSERT INTO orders (customer_id, order_date, total) VALUES (%s, %s, %s) RETURNING id", (customer_id, order_date, total))
        order_id = cursor.fetchone()['id']
        
        for item in items:
            product_id = item['product_id']
            quantity = item['quantity']
            price = item['price']
            cursor.execute("INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (%s, %s, %s, %s)", (order_id, product_id, quantity, price))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({"message": "Order placed", "order_id": order_id}), 201

    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return jsonify(orders)

if __name__ == '__main__':
    app.run(debug=True)
