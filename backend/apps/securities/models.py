from django.db import models
from .const import SECURITY_TYPE_OPTIONS, SECURITY_TYPE_OPTION_ASX_EQUITY
from .utils import format_price


class _PricingCommon(models.Model):
    class Meta:
        abstract = True

    def price_latest_price(self):
        return self.price_latest().price if self.price_latest() else None

    def price_latest_price_disp(self):
        return format_price(self.price_latest_price()) if self.price_latest() else None

    def price_latest_date(self):
        return self.price_latest().date if self.price_latest() else None


class Security(_PricingCommon, models.Model):
    code = models.CharField(max_length=255)
    security_id = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    security_type = models.CharField(max_length=2,
        choices=SECURITY_TYPE_OPTIONS, default=SECURITY_TYPE_OPTION_ASX_EQUITY)

    class Meta:
        unique_together = (('security_type', 'security_id'), ('security_type', 'code'))
        verbose_name_plural = 'Securities'

    def __str__(self):
        return '{} - {}'.format(self.description, self.code)

    def price_latest(self):
        return self.prices.all().order_by('-date').first()


class Price(_PricingCommon, models.Model):
    """
    Main Assumptions
        - you are only fetching the value once a day
        - no datetime values provided (date only)
            - Can't be used for: calculating exact buy/sell price on a transaction
            - Could be used for: historical records, current account value (estimated)? etc.
    """
    security = models.ForeignKey(Security, related_name='prices', blank=True, null=True)
    # denormalized. Ideally get data on each price's security and stuff it in a Security instance
    # also note name_clashing so can't use security_id
    id_security = models.CharField(max_length=255)
    # arbitary max digits and decimal places
    price = models.DecimalField(decimal_places=10, max_digits=30)
    date = models.DateField()

    def __str__(self):
        return "%s%s" % (self.id_security,
            ' - ' + self.security.description if self.security else '')

    def price_latest(self):
        return Price.objects.all().filter(id_security=self.id_security).order_by('-date').first()
