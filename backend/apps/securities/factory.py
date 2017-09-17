import factory
from .models import Security, Price
from .const import SECURITY_TYPE_OPTION_ASX_EQUITY


class SecurityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Security

    code = factory.Faker('pystr', min_chars=2, max_chars=4)  # so it looks like a code
    security_id = factory.Faker('ssn')
    description = factory.Faker('sentence')
    security_type = SECURITY_TYPE_OPTION_ASX_EQUITY

    @classmethod
    def _after_postgeneration(cls, obj, create, results=None):
        """Security should have 1+ Price instances to get valid data for Security.price_latest()"""
        PriceFactory.create(security=obj)


class PriceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Price

    id_security = factory.Faker('ssn')
    price = factory.Faker('pydecimal')
    date = factory.Faker('date')
    security = factory.SubFactory(SecurityFactory)
