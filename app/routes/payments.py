from flask import Blueprint, request, redirect, url_for, flash, session, current_app
import requests
import uuid
from app.utils.auth_decorators import login_required
from app.models.database import get_db_connection

payments = Blueprint('payments', __name__)

@payments.route('/pay/<int:product_id>', methods=['POST'])
@login_required
def pay(product_id):
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
    conn.close()
    if not product:
        flash('Product not found!', 'error')
        return redirect(url_for('main.index'))
    email = request.form['email']
    amount = int(product['price'] * 100)
    headers = {
        "Authorization": f"Bearer {current_app.config['PAYSTACK_SECRET_KEY']}",
        "Content-Type": "application/json"
    }
    data = {
        "email": email,
        "amount": amount,
        "reference": str(uuid.uuid4()),
        "callback_url": current_app.config['CALLBACK_URL'],
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
        return redirect(url_for('main.index')) 