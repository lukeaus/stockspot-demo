from django.db import models
from .const import SECURITY_TRADE_TYPE_OPTIONS, SECURITY_TRADE_TYPE_OPTION_BUY
from .qs import TransactionQuerySet


class Transaction(models.Model):
    """
    Record keeping for security transactions

    Main Assumptions
        * need an exact price for each trade (purely arbitary max digits and decimal palces)
        * created time in database different to transaction being executed by 3rd party services
    """
    client = models.ForeignKey('clients.Client', related_name='transactions')
    security = models.ForeignKey('securities.Security', related_name='transactions')
    trade_type = models.CharField(max_length=3, choices=SECURITY_TRADE_TYPE_OPTIONS,
        default=SECURITY_TRADE_TYPE_OPTION_BUY)
    # arbitary max digits and decimal places
    price = models.DecimalField(decimal_places=10, max_digits=30)
    market_value = models.DecimalField(decimal_places=10, max_digits=30)
    qty = models.PositiveIntegerField()
    date = models.DateField(auto_now_add=True)
    objects = TransactionQuerySet()

    def qty_vector(self):
        return self.qty if self.trade_type == SECURITY_TRADE_TYPE_OPTION_BUY else -self.qty
