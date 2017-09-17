from datetime import timedelta
from django.utils import timezone
from django.test import TestCase
from .factory import SecurityFactory, PriceFactory

class TestPricePriceLatest(TestCase):
    """Tests: Price.price_latest()"""
    def setUp(self):
        self.security = SecurityFactory.create()

    def test_multiple_prices_returns_latest(self):
        price1 = PriceFactory(security=self.security, date=timezone.now())
        PriceFactory(security=self.security, date=timezone.now() - timedelta(days=2))
        self.assertEqual(price1.price_latest(), price1)


class TestSecurityPriceLatest(TestCase):
    """Tests: Security.price_latests()"""
    def setUp(self):
        self.security = SecurityFactory.create()

    def test_multiple_prices_returns_latest(self):
        price1 = PriceFactory(security=self.security, date=timezone.now())
        PriceFactory(security=self.security, date=timezone.now() - timedelta(days=2))
        self.assertEqual(self.security.price_latest(), price1)
