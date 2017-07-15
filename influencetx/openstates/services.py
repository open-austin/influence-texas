"""
Application services for Open States interface.
"""
from collections import namedtuple
from enum import Enum

from django.core.exceptions import ValidationError

from . import utils
from influencetx.legislators import models


class Action(Enum):
    ADDED = 'Added'
    FAILED = 'Failed'
    UPDATED = 'Updated'
    SKIPPED = 'Skipped'


class ActionInfo(namedtuple('ActionInfo', ['action', 'instance', 'error'])):

    @classmethod
    def create(cls, action, instance):
        return cls(action, instance, error=None)

    @classmethod
    def fail(cls, error):
        return cls(action=Action.FAILED, instance=None, error=error)


def sync_legislator_data(data, commit=True):
    """Add, update, or ignore legislator data from Open States API.

    Args:
        data (dict): Legislator data from Open States API.
        commit (bool): Save to the database.
    Returns:
        info (ActionInfo): Action performed and legislator instance.
    """
    match = models.Legislator.objects.filter(openstates_leg_id=data['leg_id'])
    if match.exists():
        return sync_existing_legislator_data(match.first(), data, commit=commit)
    else:
        return sync_new_legislator_data(data, commit=commit)


def sync_new_legislator_data(data, commit=True):
    try:
        instance = utils.deserialize_openstates_legislator(data, commit=commit)
        return ActionInfo.create(Action.ADDED, instance)
    except KeyError as error:
        return ActionInfo.fail(f'Input legislator data missing key: {error}')
    except ValidationError as error:
        info = f'{data["first_name"]} {data["last_name"]} ({data["leg_id"]})'
        error_message = str(error)
        msg = f'Failed to add legislator, {info}, with errors {error_message}'
        return ActionInfo.fail(msg)


def sync_existing_legislator_data(instance, data, commit=True):
    new_data_date = utils.parse_datetime(data['updated_at']).date()
    if instance.openstates_updated_at.date() < new_data_date:
        instance = utils.update_legislator_instance(instance, data, commit=commit)
        return ActionInfo.create(Action.UPDATED, instance)
    else:
        return ActionInfo.create(Action.SKIPPED, instance)
