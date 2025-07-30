from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.database import get_db_connection

main = Blueprint('main', __name__)

@main.route('/')
def index():
    conn = get_db_connection()
    products = conn.execute('''
        SELECT p.*, u.username as seller_name 
        FROM products p 
        JOIN users u ON p.seller_id = u.id 
        ORDER BY p.created_at DESC
    ''').fetchall()
    conn.close()
    return render_template('index.html', products=products)

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user_type = request.form['user_type']
        if not username or not email or not password or not user_type:
            flash('All fields are required.', 'error')
            return render_template('register.html')
        if user_type not in ['buyer', 'seller']:
            flash('Invalid user type.', 'error')
            return render_template('register.html')
        conn = get_db_connection()
        existing_user = conn.execute('SELECT * FROM users WHERE username = ? OR email = ?', (username, email)).fetchone()
        if existing_user:
            flash('Username or email already exists.', 'error')
            conn.close()
            return render_template('register.html')
        password_hash = generate_password_hash(password)
        conn.execute('INSERT INTO users (username, email, password_hash, user_type) VALUES (?, ?, ?, ?)', (username, email, password_hash, user_type))
        conn.commit()
        conn.close()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html')

@main.route('/login', methods=['GET', 'POST'])
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
            return redirect(url_for('main.index'))
        else:
            flash('Invalid username or password.', 'error')
    return render_template('login.html')

@main.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))

@main.route('/payment-success')
def payment_success():
    return render_template('success.html') 