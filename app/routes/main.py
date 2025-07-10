from flask import Blueprint, render_template, flash, redirect, url_for
from ..models.product import Product

main = Blueprint('main', __name__)

@main.route('/')
def index():
    """Homepage with product listing"""
    products = Product.get_all()
    return render_template('index.html', products=products)

@main.route('/payment-success')
def payment_success():
    """Payment success page"""
    return render_template('success.html') 