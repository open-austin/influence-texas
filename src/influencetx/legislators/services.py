"""
Application services for Legislators.
"""
from collections import namedtuple
from django.core.exceptions import ValidationError
from enum import Enum
from . import models
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


def sync_legidmap_data(csv_row, options, commit=True):
    """Add or update legislatoridmap data from CSV.

    Args:
        csv_row (list): Legislatoridmap data from csv.
        commit (bool): Save to the database.
    Returns:
        info (ActionInfo): Action performed and legislator instance.
    """
    match = models.Legislator.objects.filter(openstates_leg_id=csv_row[0])
    if match.exists():
        idmap_instance = models.LegislatorIdMap.objects.filter(openstates_leg_id=csv_row[0])
        if idmap_instance.exists():
            model, created = models.LegislatorIdMap.objects.update_or_create(
                openstates_leg_id=csv_row[0],
                tpj_filer_id=csv_row[1]
            )
            #log.warn(model, created)
            if created:
                return ActionInfo.create(Action.UPDATED, model)
            else:
                return ActionInfo.create(Action.SKIPPED, model)
        else:
            model, created = models.LegislatorIdMap.objects.update_or_create(
                openstates_leg_id=csv_row[0],
                tpj_filer_id=csv_row[1]
            )
            #log.warn(model, created)
            if created:
                return ActionInfo.create(Action.ADDED, model)
            else:
                info = f"{csv_row[0]} {csv_row[1]})"
                msg = f'Failed to create legislatoridmap {info}'
                return ActionInfo.fail(msg)
    else:
        info = f"{csv_row[0]})"
        msg = f'Failed to find legislator with id {info}'
        return ActionInfo.fail(msg)
