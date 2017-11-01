import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta

from django.db import models

from influencetx.core import constants, utils
from influencetx.tpj import models as tpj_models


log = logging.getLogger(__name__)


class Legislator(models.Model):

    first_name = models.CharField(max_length=35)
    middle_name = models.CharField(max_length=35, blank=True)
    last_name = models.CharField(max_length=35)
    suffixes = models.CharField(max_length=35, blank=True)

    party = models.CharField(max_length=1, choices=constants.PARTY_CHOICES)
    chamber = models.CharField(max_length=5, choices=constants.CHAMBER_CHOICES)
    district = models.IntegerField()

    # updated_at field from Open States API. Used to check whether legislator-detail needs update.
    openstates_updated_at = models.DateTimeField()
    # Legislator ID from Open States API.
    openstates_leg_id = models.CharField(max_length=20, db_index=True)
    transparencydata_id = models.CharField(max_length=35, db_index=True, blank=True)
    votesmart_id = models.CharField(max_length=10, db_index=True, blank=True)

    # Member url at http://www.house.state.tx.us
    url = models.URLField(blank=True)
    photo_url = models.URLField(blank=True)

    @property
    def party_label(self):
        """User-friendly party label."""
        return utils.party_label(self.party)

    @property
    def chamber_label(self):
        """User-friendly label for chamber of congress."""
        return utils.chamber_label(self.chamber)

    @property
    def contributions(self, max_count=10, since=None):
        """Campaign contributions to legislator."""
        try:
            id_map = LegislatorIdMap.objects.get(openstates_leg_id=self.openstates_leg_id)
        except LegislatorIdMap.DoesNotExist:
            log.warn(f"Filer id not found for openstates leg-id {self.openstates_leg_id!r}.")
            return []
        if since is None:
            since = datetime.now() - relativedelta(years=3)
        filer = tpj_models.Filer.objects.get(id=id_map.tec_filer_id)
        contributions = (
            filer.contribution_set
            .filter(date__range=(since, datetime.now()))
            .order_by('-amount')[:max_count]
        )
        return contributions

    def __str__(self):
        name_parts = (self.first_name, self.middle_name, self.last_name, self.suffixes)
        return ' '.join(name for name in name_parts if name)


class LegislatorIdMap(models.Model):

    openstates_leg_id = models.CharField(max_length=20, db_index=True)
    tec_filer_id = models.IntegerField()
