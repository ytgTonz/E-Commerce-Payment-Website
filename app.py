from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
import requests
import uuid
import os
import sqlite3
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from functools import wraps
from app import create_app
from app.utils.auth_decorators import login_required, seller_required

app = create_app()
app.secret_key = 'your-secret-key-here'  # Change this to a secure secret key

# Configuration
PAYSTACK_SECRET_KEY = 'sk_test_a2c5d7cacf97b2bf4007a7b3e2871897198c21bf'
PAYSTACK_PUBLIC_KEY = 'pk_test_0462a4488b86d64ff1db027d0905c85fb58e4396'
CALLBACK_URL = 'http://127.0.0.1:5000/payment-success'
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def init_db():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            user_type TEXT NOT NULL CHECK (user_type IN ('buyer', 'seller')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create products table (updated with seller_id)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            image_path TEXT,
            seller_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (seller_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect('products.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    products = conn.execute('''
        SELECT p.*, u.username as seller_name 
        FROM products p 
        JOIN users u ON p.seller_id = u.id 
        ORDER BY p.created_at DESC
    ''').fetchall()
    conn.close()
    return render_template('index.html', products=products, public_key=PAYSTACK_PUBLIC_KEY)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user_type = request.form['user_type']
        
        # Validate input
        if not username or not email or not password or not user_type:
            flash('All fields are required.', 'error')
            return render_template('register.html')
        
        if user_type not in ['buyer', 'seller']:
            flash('Invalid user type.', 'error')
            return render_template('register.html')
        
        conn = get_db_connection()
        
        # Check if user already exists
        existing_user = conn.execute('SELECT * FROM users WHERE username = ? OR email = ?', 
                                   (username, email)).fetchone()
        
        if existing_user:
            flash('Username or email already exists.', 'error')
            conn.close()
            return render_template('register.html')
        
        # Create new user
        password_hash = generate_password_hash(password)
        conn.execute('INSERT INTO users (username, email, password_hash, user_type) VALUES (?, ?, ?, ?)',
                    (username, email, password_hash, user_type))
        conn.commit()
        conn.close()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['user_type'] = user['user_type']
            flash(f'Welcome back, {user["username"]}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/add-product', methods=['GET', 'POST'])
@login_required
@seller_required
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        
        # Handle image upload
        image_path = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Add timestamp to avoid filename conflicts
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"{timestamp}_{filename}"
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(filepath)
                image_path = f"uploads/{filename}"
        
        conn = get_db_connection()
        conn.execute('INSERT INTO products (name, description, price, image_path, seller_id) VALUES (?, ?, ?, ?, ?)',
                    (name, description, price, image_path, session['user_id']))
        conn.commit()
        conn.close()
        
        flash('Product added successfully!', 'success')
        return redirect(url_for('manage_products'))
    
    return render_template('add_product.html')

@app.route('/manage-products')
@login_required
@seller_required
def manage_products():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products WHERE seller_id = ? ORDER BY created_at DESC', 
                           (session['user_id'],)).fetchall()
    conn.close()
    return render_template('manage_products.html', products=products)

@app.route('/edit-product/<int:product_id>', methods=['GET', 'POST'])
@login_required
@seller_required
def edit_product(product_id):
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM products WHERE id = ? AND seller_id = ?', 
                          (product_id, session['user_id'])).fetchone()
    
    if not product:
        flash('Product not found or you do not have permission to edit it.', 'error')
        return redirect(url_for('manage_products'))
    
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        
        # Handle image upload
        image_path = product['image_path']
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"{timestamp}_{filename}"
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(filepath)
                image_path = f"uploads/{filename}"
        
        conn.execute('UPDATE products SET name = ?, description = ?, price = ?, image_path = ? WHERE id = ? AND seller_id = ?',
                    (name, description, price, image_path, product_id, session['user_id']))
        conn.commit()
        conn.close()
        
        flash('Product updated successfully!', 'success')
        return redirect(url_for('manage_products'))
    
    conn.close()
    return render_template('edit_product.html', product=product)

@app.route('/delete-product/<int:product_id>')
@login_required
@seller_required
def delete_product(product_id):
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM products WHERE id = ? AND seller_id = ?', 
                          (product_id, session['user_id'])).fetchone()
    
    if not product:
        flash('Product not found or you do not have permission to delete it.', 'error')
        return redirect(url_for('manage_products'))
    
    # Delete image file if it exists
    if product['image_path']:
        try:
            os.remove(os.path.join('static', product['image_path']))
        except:
            pass  # File might not exist
    
    conn.execute('DELETE FROM products WHERE id = ? AND seller_id = ?', 
                (product_id, session['user_id']))
    conn.commit()
    conn.close()
    
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('manage_products'))

@app.route('/pay/<int:product_id>', methods=['POST'])
@login_required
def pay(product_id):
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
    conn.close()
    
    if not product:
        flash('Product not found!', 'error')
        return redirect(url_for('index'))
    
    email = request.form['email']
    amount = int(product['price'] * 100)  # Convert to kobo (multiply by 100)

    headers = {
        "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "email": email,
        "amount": amount,
        "reference": str(uuid.uuid4()),
        "callback_url": CALLBACK_URL,
        "metadata": {
            "product_id": product_id,
            "product_name": product['name'],
            "buyer_id": session['user_id']
        }
    }

    response = requests.post("https://api.paystack.co/transaction/initialize", json=data, headers=headers)
    res_data = response.json()

    if res_data.get('status') is True:
        auth_url = res_data['data']['authorization_url']
        return redirect(auth_url)
    else:
        flash('Payment initialization failed', 'error')
        return redirect(url_for('index'))

@app.route('/payment-success')
def payment_success():
    return render_template('success.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)