from django.db import models

from influencetx.core import constants


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
    transparencydata_id = models.CharField(max_length=35, db_index=True)
    votesmart_id = models.CharField(max_length=10, db_index=True)

    # Member url at http://www.house.state.tx.us
    url = models.URLField(blank=True)
    photo_url = models.URLField(blank=True)

    def __str__(self):
        name_parts = (self.first_name, self.middle_name, self.last_name, self.suffixes)
        return ' '.join(name for name in name_parts if name)
