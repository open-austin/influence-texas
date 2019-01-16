"""
Application services for Open States interface.
"""
from collections import namedtuple
from enum import Enum

from django.core.exceptions import ValidationError

from . import utils
from influencetx.legislators import models
import logging
log = logging.getLogger(__name__)

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


def sync_legislator_data(api_data, commit=True):
    """Add, update, or ignore legislator data from Open States API.

    Args:
        api_data (dict): Legislator data from Open States API.
        commit (bool): Save to the database.
    Returns:
        info (ActionInfo): Action performed and legislator instance.
    """
    match = models.Legislator.objects.filter(openstates_leg_id=api_data['id'])
    if match.exists():
        return sync_existing_legislator_data(match.first(), api_data, commit=commit)
    else:
        return sync_new_legislator_data(api_data, commit=commit)


def sync_new_legislator_data(api_data, commit=True):
    try:
        instance = utils.deserialize_openstates_legislator(api_data, commit=commit)
        return ActionInfo.create(Action.ADDED, instance)
    except KeyError as error:
        return ActionInfo.fail(f'Input legislator data missing key: {error}')
    except ValidationError as error:
        info = f"{api_data['name']} ({api_data['id']})"
        error_message = str(error)
        msg = f'Failed to add legislator, {info}, with errors {error_message}'
        return ActionInfo.fail(msg)


def sync_existing_legislator_data(instance, api_data, commit=True):
    new_data_date = utils.parse_datetime(api_data['updatedAt']).date()
    if instance.openstates_updated_at.date() < new_data_date:
        new_instance = utils.deserialize_openstates_legislator(api_data, commit=commit)
        instance = utils.update_legislator_instance(new_instance, api_data, commit=commit)
        return ActionInfo.create(Action.UPDATED, instance)
    else:
        return ActionInfo.create(Action.SKIPPED, instance)


def sync_bill_data(api_data, force_update=False):
    instance = utils.find_matching_bill(api_data['id'])

    try:
        if instance:
            new_data_date = utils.parse_datetime(api_data['updated_at']).date()
            if instance.openstates_updated_at.date() < new_data_date or force_update:
                instance = utils.deserialize_openstates_bill(api_data, instance=instance)
                return ActionInfo.create(Action.UPDATED, instance)
            else:
                return ActionInfo.create(Action.SKIPPED, instance)
        else:
            instance = utils.deserialize_openstates_bill(api_data)
            return ActionInfo.create(Action.ADDED, instance)
    except ValidationError as error:
        info = f'{api_data["id"]} ({api_data["bill_id"]} from session {api_data["session"]})'
        error_message = str(error)
        msg = f'Failed to add bill, {info}, with errors {error_message}'
        return ActionInfo.fail(msg)
