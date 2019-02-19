"""
Django admin command wrapper around `sync_legidmap_data` in `influencetx.legislators.services`.
"""
from django.core.management.base import BaseCommand
from influencetx.legislators import services
import csv
import logging
log = logging.getLogger(__name__)


class Command(BaseCommand):

    help = 'Import legislator ID map from CSV'

    def add_arguments(self, parser):
        parser.add_argument('--max', default=200, type=int,
                            help='Max number of legislators to sync. Mainly used for testing. Default is 200.')
        parser.add_argument('--file', type=str, default=None,
                            help='CSV file containing data.')

    def handle(self, *args, **options):
        legislator_list = self._fetch_row(options)
        if not legislator_list:
            self.stdout.write(self.style.SUCCESS('No data to sync'))
            return
        total_action = 0
        for data in legislator_list:
            if total_action == 0:
                total_action += 1
                continue
            if total_action > options['max']:
                break
            # log.warn(data)
            info = services.sync_legidmap_data(data, options)
            self._write_info(info)
            total_action += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully synced {total_action - 1} legislators'))

    def _write_info(self, info):
        if info.action == services.Action.FAILED:
            action = self.style.NOTICE(info.action)
            self.stdout.write(f'{action}: {info.error}')
            raise Exception(f"Write failed with {action}: {info.error}")
        else:
            action = self.style.SUCCESS(info.action)
            legislator = info.instance
            self.stdout.write(f'{action}: {legislator.openstates_leg_id} = ({legislator.tpj_filer_id})')

    def _fetch_row(self, options):
        """Return rows from csv file."""
        with open(options['file'], newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in reader:
                yield row
