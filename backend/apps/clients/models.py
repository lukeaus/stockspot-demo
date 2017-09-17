from django.db import models
from django.contrib.auth import get_user_model
from apps.securities.models import Security
from apps.securities.utils import format_price
from apps.transactions.const import SECURITY_TRADE_TYPE_OPTION_BUY, SECURITY_TRADE_TYPE_OPTION_SELL


class Client(models.Model):
    """
    Client trading info.

    Main Assumptions
        * client_id_ is something to do with Advisor/Licensee and not a db row pk/id
        * there is some relationship between the securities and the advisor
        * clients can't short sell
    """
    user = models.OneToOneField(get_user_model())
    client_id = models.CharField(max_length=255)
    hin = models.CharField(max_length=255)
    advisor = models.ForeignKey('advisors.Advisor')

    def __str__(self):
        return '{} - Client Id{}'.format(self.user.get_full_name(), self.client_id)

    def portfolio(self):
        """
        Return the currently held securities for a client

        Warning...this could be slow over large data sets. Consider denormalising.

        :return: dictionary
        """
        portfolio = {}

        for transaction in self.transactions.all().select_related('security'):
            sec = transaction.security
            if not portfolio.get(sec.pk):
                portfolio[sec.pk] = {}
                portfolio[sec.pk]['qty'] = transaction.qty_vector()
                portfolio[sec.pk]['code'] = sec.code
                portfolio[sec.pk]['price_latest'] = sec.price_latest_price() or 0
                portfolio[sec.pk]['price_latest_display'] = sec.price_latest_price_disp()
                portfolio[sec.pk]['security_pk'] = sec.pk
            else:
                portfolio[sec.pk]['qty'] = portfolio[sec.pk]['qty'] + transaction.qty_vector()

        portfolio = self.portfolio_remove_unheld_securities(portfolio)
        return self.portfolio_add_securities_market_value(portfolio)

    def portfolio_remove_unheld_securities(self,portfolio):
        """:return: dictionary"""
        return {key: val for key, val in portfolio.items() if val['qty']}

    def portfolio_add_securities_market_value(self, portfolio):
        """
        Key Assumptions:
            * There are one or more Price instances for the Security

        :return: dictionary
        """
        for key, _ in portfolio.items():
            market_value = portfolio[key]['price_latest'] * portfolio[key]['qty']
            portfolio[key]['market_value'] = market_value
            portfolio[key]['market_value_display'] = format_price(market_value)
        return portfolio

    def portfolio_market_value(self):
        """
        Return value of currently held securities only.
        Does not include profit/loss for sold securities.

        :return: float
        """
        return sum([val['market_value'] for key, val in self.portfolio().items()])

    def portfolio_market_value_display(self):
        """:return: string"""
        return format_price(self.portfolio_market_value())

    def portfolio_buys_val(self):
        """:return: float"""
        buys_vals = self.transactions.buys().aggregate(total=models.Sum('market_value'))
        return buys_vals.get('total') or 0

    def portfolio_sells_val(self):
        """:return: float"""
        sells_vals = self.transactions.sells().aggregate(total=models.Sum('market_value'))
        return sells_vals.get('total') or 0

    def portfolio_profit(self):
        """
        Return both realised and unrealised profits (or losses).

        Considerations:
            * Client may have current holdings of a Security,
                Possibilities: paper profit/loss/flat
            * Client may have previous holdings of a Security and now has none.
                Possibilities: actualised profit/loss/flat
            * Client may have a mixture of current and past holdings of a Security
                (e.g. bought 10, sold 4, holds 6).
                Possibilities: actualised profit/loss/flat and paper profit/loss/flat

            Main Assumptions:
             * No short selling

        :return: float
        """
        return self.portfolio_sells_val() - self.portfolio_buys_val()\
            + self.portfolio_market_value()

    def portfolio_profit_display(self):
        """:return: string"""
        return format_price(self.portfolio_profit())
