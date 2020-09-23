"""
Django admin command wrapper around `sync_legislator_id` in `influencetx.tlo.services`.
"""
from django.core.management.base import BaseCommand
from django.conf import settings
from influencetx.tlo import fetch, services


class Command(BaseCommand):

    help = 'Sync legislator ids from TLO'

    def add_arguments(self, parser):
        parser.add_argument('--max', default=200, type=int,
                            help='Max number of legislators to sync. Mainly used for testing.' +
                                 'Default is 200.')
        parser.add_argument('--session', type=int, default=None,
                            help='Pull data for specified session. Defaults to settings.')
        parser.add_argument('--chamber', type=str, default=None,
                            help='Chamber to sync legislators from. Default is both.')

    def handle(self, *args, **options):
        total_action = 0
        if not options['session']:
            options['session'] = settings.TLO_SESSION
        if not options['chamber']:
            chamber_list = ['House', 'Senate']
            for chamber in chamber_list:
                options['chamber'] = chamber
                data = self._fetch_legislators(options)
                legislator_list = data[options['session']][options['chamber']]
                #self.stdout.write(f'{legislator_list}')
                if not legislator_list:
                    self.stdout.write(self.style.SUCCESS('No data to sync'))
                    return
                for record in legislator_list:
                    #self.stdout.write(f'Processing record: {record}')
                    info = services.sync_legislator_id(record, options['session'], options['chamber'])
                    self._write_info(info)
                    total_action += 1
        else:
            data = self._fetch_legislators(options)
            legislator_list = data[options['session']][options['chamber']]
            #self.stdout.write(f'{legislator_list}')
            if not legislator_list:
                self.stdout.write(self.style.SUCCESS('No data to sync'))
                return
            for record in legislator_list:
                #self.stdout.write(f'Processing record: {record}')
                info = services.sync_legislator_id(record, options['session'], options['chamber'])
                self._write_info(info)
                total_action += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully synced {total_action} legislator ids'))

    def _write_info(self, info):
        if info.action == services.Action.FAILED:
            action = self.style.NOTICE(info.action)
            self.stdout.write(f'{action}: {info.error}')
            #raise Exception(f"Write failed with {action}: {info.error}")
        else:
            action = self.style.SUCCESS(info.action)
            legislator = info.instance
            self.stdout.write(f'{action}: {legislator} ({legislator.tx_lege_id})')

    def _fetch_legislators(self, options):
        """Return list of legislator data from TLO."""
        return fetch.get_legislator_ids(options['session'], options['chamber'])
