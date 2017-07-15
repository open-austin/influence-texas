"""
Django admin command wrapper around `sync_legislator_data` in `influencetx.openstates.services`.
"""
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError

from influencetx.openstates import fetch, services
from influencetx.legislators import models


class Command(BaseCommand):

    help = 'Sync legislator data from Open States API'

    def add_arguments(self, parser):
        parser.add_argument('--max', default=None, type=int,
                            help='Max number of legislators to sync. Mainly used for testing.')
        parser.add_argument('--leg-ids', nargs='+',
                            help='Open States leg_ids of legislators to sync.')

    def handle(self, *args, **options):
        legislator_list = self._fetch_legislators(options)
        if not legislator_list:
            self.stdout.write(self.style.SUCCESS('No data to sync'))
            return

        for data in legislator_list:
            info = services.sync_legislator_data(data)
            self._write_info(info)

        self.stdout.write(self.style.SUCCESS('Successfully synced legislators'))

    def _write_info(self, info):
        if info.action == services.Action.FAILED:
            action = self.style.NOTICE(info.action)
            self.stdout.write(f'{action}: {info.error}')
        else:
            action = self.style.SUCCESS(info.action)
            legislator = info.instance
            self.stdout.write(f'{action}: {legislator} ({legislator.openstates_leg_id})')

    def _fetch_legislators(self, options):
        """Return list of legislator data from Open States API."""
        legislator_ids = options.get('leg_ids')
        legislator_list = fetch.legislators()
        if legislator_ids:
            legislator_list = [data for data in legislator_list
                               if data['leg_id'] in legislator_ids]
        return legislator_list[:options['max']]
