import factory
from .models import Licensee, Advisor


class LicenseeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Licensee

    name = factory.Faker('name')
    licensee_id = factory.Faker('ean8')


class AdvisorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Advisor

    name = factory.Faker('name')
    advisor_id = factory.Faker('ean13')
    licensee = factory.SubFactory(LicenseeFactory)
