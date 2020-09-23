"""
Application services for TLO.
"""
from collections import namedtuple
from enum import Enum
from django.core.exceptions import ValidationError
from influencetx.legislators import models
from influencetx.tlo import fetch
import logging
LOG = logging.getLogger(__name__)


class Action(Enum):
    ADDED = 'Added'
    FAILED = 'Failed'
    UPDATED = 'Updated'
    SKIPPED = 'Skipped'


class ActionInfo(namedtuple('ActionInfo', ['action', 'instance', 'error'])):

    @classmethod
    def update(cls, action, instance):
        return cls(action, instance, error=None)

    @classmethod
    def fail(cls, error):
        return cls(action=Action.FAILED, instance=None, error=error)


def sync_legislator_id(json_data, session, chamber, commit=True):
    """Add legislator id from TLO.

    Args:
        json_data (dict): Legislator data from TLO.
            (Example: {'A2100': {'name': 'Allen', 'url'...}})
        commit (bool): Save to the database.
    Returns:
        info (ActionInfo): Action performed and legislator instance.
    """
    LOG.debug(f'Processing data: {json_data}')
    id = json_data['id']
    name = json_data['name']
    if ', ' in name:
        # Duplicate last name in chamber
        name_list = name.split(', ')
        last_name = name_list[0]
        first_name = name_list[1]
        match = models.Legislator.objects.filter(chamber=chamber).filter(last_name=last_name).filter(name__icontains=first_name)
    else:
        match = models.Legislator.objects.filter(chamber=chamber).filter(last_name=name)

    if match.exists():
        #LOG.info(f'Updating legislator {match[0]}')
        return add_legislator_id(match[0], id, commit)
    else:
        msg = f'Failed to find legislator {name} in chamber {chamber}'
        return ActionInfo.fail(msg)


def add_legislator_id(instance, id, commit):
    if instance.tx_lege_id == id:
        return ActionInfo.update(Action.SKIPPED, instance)
    else:
        instance.tx_lege_id = id
        if commit:
            instance.save()
        return ActionInfo.update(Action.ADDED, instance)
