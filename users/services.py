import stripe

from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY

def create_stripe_product(prod):
    """Создает продукт в страйпе"""
    product = prod.course_paid if prod.course_paid else prod.lesson_paid
    stripe_product = stripe.Product.create(name=product)
    return stripe_product.get('id')


def create_stripe_price(amount, product_id):
    """Создает цену в Stripe"""
    return stripe.Price.create(
        currency="rub",
        unit_amount=int(amount * 100),  # Сумма в копейках
        product=product_id,  # Используем product_id вместо product_data
    )

def create_stripe_sessions(price):
    """Создает сессию на оплату в Stripe"""
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price.get('id'), "quantity": 1}],
        mode="payment",
    )
    return session.get('id'), session.get('url')
