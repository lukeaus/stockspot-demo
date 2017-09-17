from django.test import TestCase
from .factory import TransactionFactory
from .const import SECURITY_TRADE_TYPE_OPTION_BUY, SECURITY_TRADE_TYPE_OPTION_SELL


class TestTransactionQtyVector(TestCase):
    """Tests: Transaction.qty_vector()"""
    def test_transaction_qty_vector_buy(self):
        transaction = TransactionFactory(trade_type=SECURITY_TRADE_TYPE_OPTION_BUY)
        self.assertTrue(transaction.qty_vector() > 0)

    def test_transaction_qty_vector_sell(self):
        transaction = TransactionFactory(trade_type=SECURITY_TRADE_TYPE_OPTION_SELL)
        self.assertTrue(transaction.qty_vector() < 0)
