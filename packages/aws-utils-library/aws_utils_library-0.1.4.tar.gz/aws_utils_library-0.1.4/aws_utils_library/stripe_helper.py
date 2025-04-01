# aws_voucher/stripe_helper.py
import stripe
import logging
from django.conf import settings
from django.urls import reverse
from datetime import datetime
from .dynamodb import VoucherDBManager

logger = logging.getLogger(__name__)

class StripeManager:
    def __init__(self):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        self.db = VoucherDBManager()

    def create_checkout_session(self, request, cart_items):
        """Create Stripe checkout session"""
        try:
            line_items = []
            for item_id, details in cart_items.items():
                line_items.append({
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': f"{details['brand']} Voucher",
                        },
                        'unit_amount': int(float(details['amount']) * 100),
                    },
                    'quantity': 1,
                })
            
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                success_url=request.build_absolute_uri(
                    reverse('payment_success') + '?session_id={CHECKOUT_SESSION_ID}'
                ).replace('%7B', '{').replace('%7D', '}'),
                cancel_url=request.build_absolute_uri(reverse('cart')),
            )
            return session
        except Exception as e:
            logger.error(f"Error creating Stripe session: {e}")
            raise

    def handle_payment_success(self, session_id, user_email, cart_items):
        """Process successful payment"""
        try:
            # Verify payment
            session = stripe.checkout.Session.retrieve(session_id)
            if session.payment_status != 'paid':
                raise ValueError("Payment not completed")
            
            # Generate and store voucher codes
            generated_codes = []
            for voucher_id, details in cart_items.items():
                code = self._generate_voucher_code()
                self.db.put_item(
                    table_name='VoucherCode',
                    item={
                        'code_id': {'S': str(uuid.uuid4())},
                        'user_email': {'S': user_email},
                        'voucher_code': {'S': code},
                        'voucher_id': {'S': voucher_id},
                        'brand': {'S': details['brand']},
                        'amount': {'N': str(details['amount'])},
                        'expiry_date': {'S': details['expiry']},
                        'is_used': {'BOOL': False},
                        'created_at': {'S': datetime.now().isoformat()}
                    }
                )
                generated_codes.append(code)
            
            return generated_codes
        except Exception as e:
            logger.error(f"Error processing payment success: {e}")
            raise

    def _generate_voucher_code(self):
        """Generate random voucher code"""
        import random
        import string
        chars = string.ascii_uppercase + string.digits
        return ''.join(random.choices(chars, k=8))