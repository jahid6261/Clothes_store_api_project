import requests

from src.utils.settings import settings


class SSLCommerz:

    def __init__(self):
        self.store_id = settings.SSLCOMMERZ_STORE_ID
        self.store_password = settings.SSLCOMMERZ_STORE_PASSWORD

        self.payment_url = settings.SSLCOMMERZ_PAYMENT_URL
        self.validation_url = settings.SSLCOMMERZ_VALIDATION_URL

        self.success_url = settings.SSLCOMMERZ_SUCCESS_URL
        self.fail_url = settings.SSLCOMMERZ_FAIL_URL
        self.cancel_url = settings.SSLCOMMERZ_CANCEL_URL


    def create_payment(self, payload: dict):

        response = requests.post(
            self.payment_url,
            data=payload,
            timeout=30
        )

        response.raise_for_status()

        return response.json()