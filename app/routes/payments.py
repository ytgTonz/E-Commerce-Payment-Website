from flask import Blueprint, request, flash, redirect, url_for
from ..models.product import Product
from ..utils.payment_utils import initialize_payment

payments = Blueprint('payments', __name__)

@payments.route('/pay/<int:product_id>', methods=['POST'])
def pay(product_id):
    """Process payment for a product"""
    product = Product.get_by_id(product_id)
    
    if not product:
        flash('Product not found!', 'error')
        return redirect(url_for('main.index'))
    
    email = request.form['email']
    
    # Initialize payment
    payment_result = initialize_payment(
        product_id=product.id,
        product_name=product.name,
        amount=product.price,
        email=email
    )
    
    if payment_result['success']:
        return redirect(payment_result['auth_url'])
    else:
        flash(f'Payment initialization failed: {payment_result["error"]}', 'error')
        return redirect(url_for('main.index')) 