import factory
from .models import User


TEST_USER_PASSWORD = 'test1234'


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker('name')
    last_name = factory.Faker('name')
    email = factory.Faker('email')
    dob = factory.Faker('date')
    password = TEST_USER_PASSWORD
    is_active = True
    is_staff = False
    is_superuser = False
