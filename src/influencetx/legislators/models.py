from django.db import models
from influencetx.core import constants, utils
import logging
log = logging.getLogger(__name__)


class Legislator(models.Model):
    # Legislator ID from Open States API.
    openstates_leg_id = models.CharField(max_length=48, db_index=True)
    name = models.CharField(max_length=45)
    first_name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=20, blank=True)
    party = models.CharField(max_length=1, choices=constants.PARTY_CHOICES)
    chamber = models.CharField(max_length=6, choices=constants.CHAMBER_CHOICES)
    district = models.IntegerField()
    # updated_at field from Open States API. Used to check whether legislator-detail needs update
    openstates_updated_at = models.DateTimeField()
    url = models.URLField(blank=True)
    photo_url = models.URLField(blank=True)

    @property
    def initial(self):
        """First initial used for placeholder image."""
        return self.name[0]

    @property
    def party_label(self):
        """User-friendly party label."""
        return utils.party_label(self.party)

    @property
    def chamber_label(self):
        """User-friendly label for chamber of congress."""
        return utils.chamber_label(self.chamber)

    def __str__(self):
        return self.name


class LegislatorIdMap(models.Model):
    # Provide mapping between TPJ FILER_ID and Legislator ID from Open States API.
    openstates_leg_id = models.CharField(max_length=48, db_index=True)
    tpj_filer_id = models.IntegerField(db_index=True)

    def __str__(self):
        return f'{self.openstates_leg_id!r} {self.tpj_filer_id}'
