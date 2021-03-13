"""
Django admin command wrapper around `sync_bill_data` in `influencetx.openstates.services`.
"""
from django.core.management.base import BaseCommand

from influencetx.openstates import fetch, services


class Command(BaseCommand):

    help = 'Sync bills data from Open States API'

    def add_arguments(self, parser):
        parser.add_argument('--max', default=0, type=int,
                            help='Max number of bills to sync. Mainly used for testing.')
        parser.add_argument('--force-update', action='store_true', default=False,
                            help='Force update, even if database is up-to-date.')
        parser.add_argument('--session', type=str, default=87,
                            help='Pull data for specified session. Defaults to most recent.')
        parser.add_argument('--start', type=str, default=None,
                            help='Start pulling data from OpenState cursor. Defaults to None.')

    def handle(self, *args, **options):
        total_bill_count = 0
        if options['start']:
            start_token = options['start']
        else:
            start_token = ''
        loop = 0
        while loop < 100:
            bill_list = self._fetch_bills(start_token, options)
            if not bill_list:
                self.stdout.write(self.style.SUCCESS('No data to sync'))
                return
            bills_total = bill_list.pop()
            start_token = bill_list.pop()
            total_count = options['max'] if options['max'] > 0 else bills_total
            print(f'Processing {len(bill_list)} bills in loop #{loop}. Next cursor: {start_token}')
            for data in bill_list:
                info = services.sync_bill_data(data, options['force_update'])
                self._write_info(info)
                total_bill_count += 1
                if total_count == total_bill_count:
                    break

            loop += 1
            if total_bill_count >= total_count:
                self.stdout.write(self.style.SUCCESS(f'Reached the maximum bill count of' +
                                                     '{total_bill_count}/{total_count}'))
                loop = 100

            if not start_token:
                self.stdout.write(self.style.SUCCESS(f'Reached the end of bill pages.'))
                loop = 100

        self.stdout.write(self.style.SUCCESS(f'Successfully synced {total_bill_count} bills'))
        return

    def _write_info(self, info):
        if info.action == services.Action.FAILED:
            action = self.style.NOTICE(info.action)
            self.stdout.write(f'{action}: {info.error}')
        else:
            action = self.style.SUCCESS(info.action)
            bill = info.instance
            self.stdout.write(f'{action}: {bill}')

    def _fetch_bills(self, startCursor, options):
        """Return list of bill data from Open States API."""
        # print(f'Requesting {options["Max"]} starting at cursor: {startCursor}')
        return fetch.bills(startCursor, options)
