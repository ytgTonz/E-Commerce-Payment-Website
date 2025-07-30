from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from datetime import datetime
import os
from app.utils.auth_decorators import login_required, seller_required
from app.models.database import get_db_connection
from app.utils.file_utils import allowed_file

products = Blueprint('products', __name__)

@products.route('/add-product', methods=['GET', 'POST'])
@login_required
@seller_required
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        image_path = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"{timestamp}_{filename}"
                filepath = os.path.join('static/uploads', filename)
                file.save(filepath)
                image_path = f"uploads/{filename}"
        conn = get_db_connection()
        conn.execute('INSERT INTO products (name, description, price, image_path, seller_id) VALUES (?, ?, ?, ?, ?)', (name, description, price, image_path, session['user_id']))
        conn.commit()
        conn.close()
        flash('Product added successfully!', 'success')
        return redirect(url_for('products.manage_products'))
    return render_template('add_product.html')

@products.route('/manage-products')
@login_required
@seller_required
def manage_products():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products WHERE seller_id = ? ORDER BY created_at DESC', (session['user_id'],)).fetchall()
    conn.close()
    return render_template('manage_products.html', products=products)

@products.route('/edit-product/<int:product_id>', methods=['GET', 'POST'])
@login_required
@seller_required
def edit_product(product_id):
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM products WHERE id = ? AND seller_id = ?', (product_id, session['user_id'])).fetchone()
    if not product:
        flash('Product not found or you do not have permission to edit it.', 'error')
        return redirect(url_for('products.manage_products'))
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        image_path = product['image_path']
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"{timestamp}_{filename}"
                filepath = os.path.join('static/uploads', filename)
                file.save(filepath)
                image_path = f"uploads/{filename}"
        conn.execute('UPDATE products SET name = ?, description = ?, price = ?, image_path = ? WHERE id = ? AND seller_id = ?', (name, description, price, image_path, product_id, session['user_id']))
        conn.commit()
        conn.close()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('products.manage_products'))
    conn.close()
    return render_template('edit_product.html', product=product)

@products.route('/delete-product/<int:product_id>')
@login_required
@seller_required
def delete_product(product_id):
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM products WHERE id = ? AND seller_id = ?', (product_id, session['user_id'])).fetchone()
    if not product:
        flash('Product not found or you do not have permission to delete it.', 'error')
        return redirect(url_for('products.manage_products'))
    if product['image_path']:
        try:
            os.remove(os.path.join('static', product['image_path']))
        except:
            pass
    conn.execute('DELETE FROM products WHERE id = ? AND seller_id = ?', (product_id, session['user_id']))
    conn.commit()
    conn.close()
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('products.manage_products')) 