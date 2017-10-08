"""
Django admin command wrapper around `sync_bill_data` in `influencetx.openstates.services`.
"""
from django.core.management.base import BaseCommand

from influencetx.openstates import fetch, services


class Command(BaseCommand):

    help = 'Sync bills data from Open States API'

    def add_arguments(self, parser):
        parser.add_argument('--max', default=None, type=int,
                            help='Max number of bills to sync. Mainly used for testing.')
        parser.add_argument('--force-update', action='store_true', default=False,
                            help='Force update, even if database is up-to-date.')
        parser.add_argument('--session', type=int, default=None,
                            help='Pull data for specified session. Defaults to most recent.')

    def handle(self, *args, **options):
        bill_list = self._fetch_bills(options)
        if not bill_list:
            self.stdout.write(self.style.SUCCESS('No data to sync'))
            return

        force_update = options['force_update']
        for data in bill_list:
            bill_detail = fetch.bill_detail(data['session'], data['bill_id'])

            if hasattr(bill_detail, 'status_code'):
                response = bill_detail
                info = services.ActionInfo.fail(f'{response.status_code}: {response.reason}')
                self._write_info(info)
                continue

            info = services.sync_bill_data(bill_detail, force_update=force_update)
            self._write_info(info)

        self.stdout.write(self.style.SUCCESS('Successfully synced bills'))

    def _write_info(self, info):
        if info.action == services.Action.FAILED:
            action = self.style.NOTICE(info.action)
            self.stdout.write(f'{action}: {info.error}')
        else:
            action = self.style.SUCCESS(info.action)
            bill = info.instance
            self.stdout.write(f'{action}: {bill} ({bill.openstates_bill_id}, {bill.bill_id})')

    def _fetch_bills(self, options):
        """Return list of bill data from Open States API."""
        bill_count = options['max'] or fetch.DEFAULT_BILL_COUNT
        if options['session']:
            search_window = 'session:{}'.format(options['session'])
        else:
            search_window = 'session'
        return fetch.bills(per_page=bill_count, search_window=search_window)
