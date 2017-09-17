from django.test import TestCase
from .factory import UserFactory

class TestUserFullName(TestCase):
    """Tests: User.get_full_name()"""
    def setUp(self):
        self.user = UserFactory.create()

    def test_user_full_name_has_first_name_last_name(self):
        self.assertEqual(self.user.get_full_name(),
            '{} {}'.format(self.user.first_name, self.user.last_name))
