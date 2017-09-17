from django.db import models
from django.db.models import Sum
from .const import SECURITY_TRADE_TYPE_OPTION_BUY, SECURITY_TRADE_TYPE_OPTION_SELL


class TransactionQuerySet(models.Manager):
    def buys(self):
        return self.filter(trade_type=SECURITY_TRADE_TYPE_OPTION_BUY)

    def sells(self):
        return self.filter(trade_type=SECURITY_TRADE_TYPE_OPTION_SELL)
