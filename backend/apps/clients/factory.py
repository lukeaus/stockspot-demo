import factory
from .models import Client
from apps.users.factory import UserFactory
from apps.advisors.factory import AdvisorFactory


class ClientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Client

    user = factory.SubFactory(UserFactory)
    client_id = factory.Faker('ean8')
    hin = factory.Faker('ean8')
    advisor = factory.SubFactory(AdvisorFactory)
