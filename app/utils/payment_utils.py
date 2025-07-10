import requests
import uuid
from flask import current_app

def initialize_payment(product_id, product_name, amount, email):
    """Initialize payment with Paystack"""
    headers = {
        "Authorization": f"Bearer {current_app.config['PAYSTACK_SECRET_KEY']}",
        "Content-Type": "application/json"
    }

    data = {
        "email": email,
        "amount": int(amount * 100),  # Convert to kobo
        "reference": str(uuid.uuid4()),
        "callback_url": current_app.config['CALLBACK_URL'],
        "metadata": {
            "product_id": product_id,
            "product_name": product_name
        }
    }

    try:
        response = requests.post(
            "https://api.paystack.co/transaction/initialize", 
            json=data, 
            headers=headers
        )
        res_data = response.json()

        if res_data.get('status') is True:
            return {
                'success': True,
                'auth_url': res_data['data']['authorization_url'],
                'reference': res_data['data']['reference']
            }
        else:
            return {
                'success': False,
                'error': res_data.get('message', 'Payment initialization failed')
            }
    except Exception as e:
        return {
            'success': False,
            'error': f'Network error: {str(e)}'
        } 