from flask import Blueprint, render_template, request, flash, redirect, url_for
from ..models.product import Product
from ..utils.file_utils import save_uploaded_file, delete_file

products = Blueprint('products', __name__)

@products.route('/add-product', methods=['GET', 'POST'])
def add_product():
    """Add new product"""
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        
        # Handle image upload
        image_path = None
        if 'image' in request.files:
            image_path = save_uploaded_file(request.files['image'])
        
        # Create and save product
        product = Product(
            name=name,
            description=description,
            price=price,
            image_path=image_path
        )
        product.save()
        
        flash('Product added successfully!', 'success')
        return redirect(url_for('products.manage_products'))
    
    return render_template('add_product.html')

@products.route('/manage-products')
def manage_products():
    """Manage products page"""
    products_list = Product.get_all()
    stats = Product.get_stats()
    return render_template('manage_products.html', products=products_list, stats=stats)

@products.route('/edit-product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    """Edit existing product"""
    product = Product.get_by_id(product_id)
    
    if not product:
        flash('Product not found!', 'error')
        return redirect(url_for('products.manage_products'))
    
    if request.method == 'POST':
        product.name = request.form['name']
        product.description = request.form['description']
        product.price = float(request.form['price'])
        
        # Handle image upload
        if 'image' in request.files:
            new_image_path = save_uploaded_file(request.files['image'])
            if new_image_path:
                # Delete old image if exists
                if product.image_path:
                    delete_file(product.image_path)
                product.image_path = new_image_path
        
        product.save()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('products.manage_products'))
    
    return render_template('edit_product.html', product=product)

@products.route('/delete-product/<int:product_id>')
def delete_product(product_id):
    """Delete product"""
    product = Product.get_by_id(product_id)
    
    if not product:
        flash('Product not found!', 'error')
        return redirect(url_for('products.manage_products'))
    
    # Delete image file if exists
    if product.image_path:
        delete_file(product.image_path)
    
    # Delete product from database
    product.delete()
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('products.manage_products')) 