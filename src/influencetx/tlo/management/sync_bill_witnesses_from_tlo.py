"""
Django admin command wrapper around `sync_bill_data` in `influencetx.openstates.services`.
"""
from django.core.management.base import BaseCommand

from influencetx.openstates import fetch, services


class Command(BaseCommand):

    help = 'Sync bill witness data from Texas Legislature Online'

    def handle(self, *args, **options):
        bill_id = 123
        print "hello wurld!"
