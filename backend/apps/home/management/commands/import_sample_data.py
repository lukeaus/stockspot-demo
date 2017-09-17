import os
import random
from datetime import timedelta
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from django.utils import timezone
from pyexcel_xlsx import get_data
from apps.securities.models import Security, Price
from apps.securities.const import SECURITY_TYPE_OPTIONS
from apps.transactions.const import SECURITY_TRADE_TYPE_OPTIONS
from apps.advisors.models import Licensee, Advisor
from apps.clients.models import Client
from apps.transactions.models import Transaction
from ...utils import walk_up_folder


class Command(BaseCommand):
    help = 'Prefetch some example company data'

    def handle(self, *args, **options):
        file_folder_path = walk_up_folder(os.path.dirname(__file__ ), 5)
        file_path = os.path.abspath(
            os.path.join(file_folder_path, 'sample_data.xlsx'))
        data = get_data(file_path)

        #TODO: this process is brittle, relies on order of columns not being changed
        for i, entry in enumerate(data['Trading']):
            if i > 0:
                licensee = create_licensee(entry)
                advisor = create_advisor(entry, licensee)
                user = create_user(entry)
                client = create_client(entry, user, advisor)
                security = create_security(entry)
                create_transaction(entry, client, security)

        for i, entry in enumerate(data['Security Prices']):
            if i > 0:
                create_price(entry)


def create_user(entry):
    """Make a user and generate required data for fields not in sample data."""
    # only works for first + last name currently
    full_name = entry[5].split()
    email = '{first_name}-{client_id}@{domain}'.format(
        first_name=full_name[0].lower(),
        client_id=str(entry[4]).strip(),  # unique email for clients with same name
        domain='example.com')
    password = 'test1234'
    dob = timezone.now() - timedelta(days=(365 * random.randint(18, 99)))
    try:
        user = get_user_model().objects.get(email=email)
    except get_user_model().DoesNotExist:
        user = get_user_model().objects.create_user(email=email, first_name=full_name[0],
            last_name=full_name[1], password=password, dob=dob)
    return user


def get_or_create_obj(class_, data):
    """Cause models.Model.objects.get_or_create() can be finicky"""
    try:
        obj = class_.objects.get(**data)
    except class_.DoesNotExist:
        obj = class_.objects.create(**data)
    return obj


def create_client(entry, user, advisor):
    data = {
        'user': user,
        'client_id': str(entry[4]).strip(),
        'hin': str(entry[10]).strip(),
        'advisor': advisor
    }
    return get_or_create_obj(Client, data)


def create_licensee(entry):
    data = {
        'name': entry[1].strip(),
        'licensee_id': str(entry[0]).strip()
    }
    return get_or_create_obj(Licensee, data)


def create_security(entry):
    security_type = [e[0] for e in SECURITY_TYPE_OPTIONS if entry[11].strip() == e[1]][0]
    data = {
        'code': entry[6].strip(),
        'security_id': str(entry[7]).strip(),
        'description': entry[8].strip(),
        'security_type': security_type
    }
    return get_or_create_obj(Security, data)


def create_transaction(entry, client, security):
    trade_type = [
        e[0] for e in SECURITY_TRADE_TYPE_OPTIONS if entry[12].strip().lower() == e[1].lower()][0]
    market_value = float(entry[14])  # already a float
    price = float(entry[13])  # already a float
    qty = int(round(market_value / price))  # approximation... see Transaction model notes

    data = {
        'client': client,
        'security': security,
        'trade_type': trade_type,
        'price': price,
        'market_value': market_value,
        'date': entry[15].date(),  # automagically arrives as a datetime object
        'qty': qty
    }

    #TODO: make function idempotent...something non-obvious (to LMS) is going on here...
    get_or_create_obj(Transaction, data)

def create_advisor(entry, licensee):
    data = {
        'advisor_id': str(entry[2]).strip(),
        'name': entry[3].strip(),
        'licensee': licensee
    }
    return get_or_create_obj(Advisor, data)


def create_price(entry):
    code = entry[0].strip()
    data = {
        'security': Security.objects.filter(code=code).first(),  # hacky
        'id_security': str(entry[0]).strip(),
        'price': float(entry[1].strip()),
        'date': datetime.strptime(entry[2].strip(), '%Y-%m-%d').date()
    }
    get_or_create_obj(Price, data)
