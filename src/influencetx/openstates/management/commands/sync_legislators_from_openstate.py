"""
Django admin command wrapper around `sync_legislator_data` in `influencetx.openstates.services`.
"""
from django.core.management.base import BaseCommand

from influencetx.openstates import fetch, services


class Command(BaseCommand):

    help = 'Sync legislators data from Open States API'

    def add_arguments(self, parser):
        parser.add_argument('--max', default=200, type=int,
                            help='Max number of legislators to sync. Mainly used for testing. Default is 200.')
        parser.add_argument('--leg-ids', nargs='+',
                            help='Open States ocd ids of legislators to sync. Defaults to all.')
        parser.add_argument('--session', type=int, default=None,
                            help='Pull data for specified session. Defaults to most recent.')
        parser.add_argument('--force-update', action='store_true', default=False,
                            help='Force update, even if database is up-to-date.')

    def handle(self, *args, **options):
        legislator_list = self._fetch_legislators(options)
        if not legislator_list:
            self.stdout.write(self.style.SUCCESS('No data to sync'))
            return
        total_action=0
        for data in legislator_list:
            info = services.sync_legislator_data(data, options)
            self._write_info(info)
            total_action+=1

        self.stdout.write(self.style.SUCCESS(f'Successfully synced {total_action} legislators'))

    def _write_info(self, info):
        if info.action == services.Action.FAILED:
            action = self.style.NOTICE(info.action)
            self.stdout.write(f'{action}: {info.error}')
            raise Exception(f"Write failed with {action}: {info.error}")
        else:
            action = self.style.SUCCESS(info.action)
            legislator = info.instance
            self.stdout.write(f'{action}: {legislator} ({legislator.openstates_leg_id})')

    def _fetch_legislators(self, options):
        """Return list of legislator data from Open States API."""
        legislator_ids = options.get('leg_ids') if options.get('leg_ids') else fetch.legislator_ids(options)
        return fetch.legislator_list(legislator_ids)
