import uuid
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


# from: https://raw.githubusercontent.com/iraycd/django-react-starter/starter/backend/accounts/models.py

class UserManager(BaseUserManager):
    def _create_user(self, email, password, first_name, last_name, is_staff, is_superuser,
            **extra_fields):
        """
        Create and save an User with the given email, password, name and phone number.

        :param email: string
        :param password: string
        :param first_name: string
        :param last_name: string
        :param is_staff: boolean
        :param is_superuser: boolean
        :param extra_fields:
        :return: User
        """
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(email=email,
                          first_name=first_name,
                          last_name=last_name,
                          is_staff=is_staff,
                          is_active=True,
                          is_superuser=is_superuser,
                          last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, first_name, last_name, password, **extra_fields):
        """
        Create and save an User with the given email, password and name.

        :param email: string
        :param first_name: string
        :param last_name: string
        :param password: string
        :param extra_fields:
        :return: User
        """
        return self._create_user(email, password, first_name, last_name, is_staff=False,
            is_superuser=False, **extra_fields)

    def create_superuser(self, email, first_name='', last_name='', password=None, **extra_fields):
        """
        Create a super user.

        :param email: string
        :param first_name: string
        :param last_name: string
        :param password: string
        :param extra_fields:
        :return: User
        """
        return self._create_user(email, password, first_name, last_name, is_staff=True,
            is_superuser=True, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Main Assumptions
        - Regular first + last name (required)
        - Middle name not required
    """
    first_name = models.CharField(_('First Name'), max_length=255, blank=True)
    middle_name = models.CharField(_('Middle Name'), max_length=255, blank=True)
    last_name = models.CharField(_('Last Name'), max_length=255, blank=True)
    email = models.EmailField(_('Email address'), unique=True)
    dob = models.DateField(blank=True, null=True)

    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_superuser = models.BooleanField(_('superuser status'), default=False)

    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    date_updated = models.DateTimeField(_('date updated'), auto_now=True)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return "{0} {1}".format(self.first_name, self.last_name)

    def get_short_name(self):
        return self.first_name
