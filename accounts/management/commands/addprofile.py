from django.core.management.base import BaseCommand
from accounts.models import Profile
from django.contrib.auth.models import User

def add_user_profile():
    users = User.objects.filter(profile=None)
    for user in users:
        Profile.objects.get_or_create(owner=user)

class Command(BaseCommand):
    help = 'Create profile for those who has not profile yet.'
    def handle(self, *args, **options):
        return add_user_profile()