from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from farm.models import Farm

def add_farm_user(username):
    qs = User.objects.filter(username=username)
    if qs.exists():
        user = qs.first()
        farms = Farm.objects.filter(user=None)
        for farm in farms:
            farm.user = user
            farm.save()

class Command(BaseCommand):
    help = 'Add user to the farms those not have user.'

    def add_arguments(self, parser):
        parser.add_argument('phone', type=str)

    def handle(self, *args, **options):
        return add_farm_user(options['phone'])