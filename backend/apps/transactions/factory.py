import factory
import factory.fuzzy
from apps.clients.factory import ClientFactory
from apps.securities.factory import SecurityFactory
from .models import Transaction
from .const import SECURITY_TRADE_TYPE_OPTIONS_VALS


class TransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Transaction

    client = factory.SubFactory(ClientFactory)
    security = factory.SubFactory(SecurityFactory)
    trade_type = factory.fuzzy.FuzzyChoice(SECURITY_TRADE_TYPE_OPTIONS_VALS)
    price = factory.Faker('pyfloat', positive=True)
    qty = factory.Faker('pyint')
    market_value = factory.LazyAttribute(lambda o: o.price * o.qty)
    date = factory.Faker('date')
