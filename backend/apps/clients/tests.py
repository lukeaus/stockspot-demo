import json
from decimal import Decimal
from math import isclose
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from apps.transactions.factory import TransactionFactory
from apps.transactions.const import SECURITY_TRADE_TYPE_OPTION_BUY, SECURITY_TRADE_TYPE_OPTION_SELL
from apps.users.factory import TEST_USER_PASSWORD
from .factory import ClientFactory


IS_CLOSE_RELATIVE_TOLERANCE = 1e-04


class TestPortfolioMarketValue(TestCase):
    """Tests: Client.portfolio_market_value()"""
    def setUp(self):
        self.client = ClientFactory.create()

    def test_single_transaction_buy(self):
        trans = TransactionFactory.create(
            client=self.client,
            trade_type=SECURITY_TRADE_TYPE_OPTION_BUY,)
        self.assertEqual(self.client.portfolio_market_value(),
            trans.security.price_latest_price() * trans.qty)

    def test_multiple_transactions_one_security_buy_sell(self):
        buy_sell_qty_diff = 5
        trans_1 = TransactionFactory.create(
            client=self.client,
            trade_type=SECURITY_TRADE_TYPE_OPTION_BUY,)
        TransactionFactory.create(
            client=self.client,
            trade_type=SECURITY_TRADE_TYPE_OPTION_SELL,
            security=trans_1.security,
            qty=trans_1.qty - buy_sell_qty_diff,
        )
        # only 1 security so should be the market_price
        self.assertEqual(self.client.portfolio_market_value(),
            trans_1.security.price_latest_price() * buy_sell_qty_diff)

    def test_multiple_transactions_multiple_securities_buy_sell(self):
        trans_1_2_buy_sell_qty_diff = 5
        trans_1 = TransactionFactory.create(
            client=self.client,
            trade_type=SECURITY_TRADE_TYPE_OPTION_BUY,)
        TransactionFactory.create(
            client=self.client,
            trade_type=SECURITY_TRADE_TYPE_OPTION_SELL,
            security=trans_1.security,
            qty=trans_1.qty - trans_1_2_buy_sell_qty_diff,
        )
        trans_3 = TransactionFactory.create(
            client=self.client,
            trade_type=SECURITY_TRADE_TYPE_OPTION_BUY,
        )

        mkt_val = trans_1_2_buy_sell_qty_diff * trans_1.security.price_latest_price() \
            + trans_3.security.price_latest_price() * trans_3.qty

        self.assertEqual(self.client.portfolio_market_value(), mkt_val)


class TestPortfolioProfitSingleSecurity(TestCase):
    """
        Tests: Client.portfolio_profit()

        Testing Conditions:
            - Single security
            - One or more buys/sells of a security
    """
    def setUp(self):
        self.client = ClientFactory.create()

    def test_unrealised_profits(self):
        trans_buy = TransactionFactory.create(
            client=self.client,
            trade_type=SECURITY_TRADE_TYPE_OPTION_BUY,)

        self.assertTrue(
            isclose(float(self.client.portfolio_profit()),
                float(trans_buy.security.price_latest_price()) * trans_buy.qty -
                float(trans_buy.market_value),
                rel_tol=IS_CLOSE_RELATIVE_TOLERANCE
            )
        )

    def test_unrealised_profits_real_numbers(self):
        """Test using some actual numbers for sanity"""
        buy_price = Decimal(2)
        current_price = Decimal(3)
        qty = 10
        trans_buy = TransactionFactory.create(
            client=self.client,
            trade_type=SECURITY_TRADE_TYPE_OPTION_BUY,
            price=buy_price,
            qty=qty,
            market_value=buy_price * qty)

        # set the latest price that you want
        price = trans_buy.security.price_latest()
        price.price = current_price
        price.save()

        self.assertEqual(float(self.client.portfolio_profit()),
            qty * (current_price - buy_price)
        )

    def test_realised_profits_sold_some_holdings(self):
        buy_sell_diff = 1
        trans_buy = TransactionFactory.create(
            client=self.client,
            trade_type=SECURITY_TRADE_TYPE_OPTION_BUY,)

        trans_sell = TransactionFactory.create(
            client=self.client,
            trade_type=SECURITY_TRADE_TYPE_OPTION_SELL,
            security=trans_buy.security,
            qty=trans_buy.qty - buy_sell_diff,
            )

        self.assertTrue(
            isclose(
                float(self.client.portfolio_profit()),
                float(trans_sell.market_value) -
                float(trans_buy.market_value) +
                float(trans_buy.security.price_latest_price()) * buy_sell_diff,
                rel_tol=IS_CLOSE_RELATIVE_TOLERANCE
            )
        )

    def test_realised_profits_sold_all_holdings(self):
        trans_buy = TransactionFactory.create(
            client=self.client,
            trade_type=SECURITY_TRADE_TYPE_OPTION_BUY,)

        trans_sell = TransactionFactory.create(
            client=self.client,
            trade_type=SECURITY_TRADE_TYPE_OPTION_SELL,
            security=trans_buy.security,
            qty=trans_buy.qty,
            )

        self.assertTrue(
            isclose(
                float(self.client.portfolio_profit()),
                float(trans_sell.market_value) - float(trans_buy.market_value),
                rel_tol=IS_CLOSE_RELATIVE_TOLERANCE
            )
        )


class TestClientViewSetList(TestCase):
    """
    Tests ClientViewSet ListView
    #TODO: reverse urls rather than hardcode
    """
    def setUp(self):
        self.test_client = APIClient()

    def test_unauthenticated_client(self):
        response = self.test_client.get('/api/clients/', format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_client(self):
        client = ClientFactory()
        self.test_client.force_authenticate(client.user)
        response = self.test_client.get('/api/clients/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestClientViewSetDetail(TestCase):
    """
    Tests ClientViewSet DetailView
    #TODO: reverse urls rather than hardcode
    """
    def setUp(self):
        self.test_client = APIClient()

    def test_unauthenticated_client(self):
        response = self.test_client.get('/api/clients/1/', format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_client_get_own_data_if_authenticated(self):
        client = ClientFactory()
        self.test_client.force_authenticate(client.user)

        # create a transaction and a new price so we have some data
        trans_buy = TransactionFactory.create(client=client)

        # set the latest price that you want so that we have a profit/loss
        price = trans_buy.security.price_latest()
        price.price = Decimal(99)
        price.save()

        # check that we created data correctly
        self.assertTrue(client.portfolio_market_value())
        self.assertTrue(client.portfolio_profit())

        # get the response
        response = self.test_client.get('/api/clients/{}/'.format(client.id), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_partial_response_data = {
            'id': client.id,
            'portfolio_market_value': client.portfolio_market_value(),
            'portfolio_profit': client.portfolio_profit()
        }

        self.assertDictContainsSubset(expected_partial_response_data, response.data)
