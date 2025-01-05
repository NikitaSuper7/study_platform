import stripe
from rest_framework import status

from config.settings import STRIPE_API_KEY, CURR_API_KEY, CURR_API_URL
import requests

stripe.api_key = STRIPE_API_KEY


def convert_price(amount):
    """Конвертирует рубли в доллары."""

    usd_price = 0
    # Забираем курс с currencyapi:
    response = requests.get(url=f"{CURR_API_URL}v3/latest?apikey={CURR_API_KEY}&currencies=RUB")
    print(response.json())
    if response.status_code == status.HTTP_200_OK:
        usd_rate = response.json()['data']['RUB'].get("value")
        usd_price = amount / usd_rate
    return int(usd_price)


def create_stripe_price(amount):
    return stripe.Price.create(
        currency="usd",
        unit_amount= int(amount * 100),
        # recurring={"interval": "month"}, # Переодическая оплата (подписка)
        product_data={"name": "Payment"},
    )


def create_stripe_session(price):
    """Создает сессию на оплату в stripe"""
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")