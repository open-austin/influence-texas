from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from django.forms.models import model_to_dict

from ... import fetch
from ... import utils
from influencetx.legislators import models


class Command(BaseCommand):

    help = 'Sync legislator data from Open States API'

    def add_arguments(self, parser):
        parser.add_argument('--max', default=None, type=int,
                            help='Max number of legislators to sync. Mainly used for testing.')
        parser.add_argument('--leg-ids', nargs='+',
                            help='Open States leg_ids of legislators to sync.')

    def handle(self, *args, **options):
        for data in self._fetch_legislators(options):
            match = models.Legislator.objects.filter(openstates_leg_id=data['leg_id'])
            if match.exists():
                instance = match.first()
                new_data_date = utils.parse_datetime(data['updated_at']).date()
                if instance.openstates_updated_at.date() < new_data_date:
                    combined_data = model_to_dict(instance)
                    combined_data.update(data)
                    instance = utils.deserialize_openstates_legislator(combined_data)
                    self._write_action('Updated', instance)
                else:
                    self._write_action('Skipped existing', instance)
            else:
                try:
                    instance = utils.deserialize_openstates_legislator(data, commit=True)
                    self._write_action('Added', instance)
                except ValidationError as error:
                    info = f'{data["first_name"]} {data["last_name"]} ({data["leg_id"]})'
                    error_message = str(error)
                    msg = f'Failed to add legislator, {info}, with errors {error_message}'
                    self.stdout.write(self.style.NOTICE(msg))

        self.stdout.write(self.style.SUCCESS('Successfully synced legislators'))

    def _write_action(self, action, legislator):
        action = self.style.SUCCESS(action)
        self.stdout.write(f'{action}: {legislator} ({legislator.openstates_leg_id})')

    def _fetch_legislators(self, options):
        """Return list of legislator data from Open States API"""
        legislator_id = options.get('leg_id')
        if legislator_id is not None:
            return [fetch.legislators(legislator_id)]
        else:
            return fetch.legislators()[:options['max']]
