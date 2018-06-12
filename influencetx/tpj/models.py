"""
TPJ models built from inspecting the TPJ database.

This contains models that are not managed by Django (in fact, TPJ database is readonly):
https://docs.djangoproject.com/en/1.11/ref/models/options/#managed.

You can generate a model from the database using the `inspectdb` management command. For example,
the Contributor model was created using the following command:

  ./djadmin.sh inspectdb --database tpj vIdealContributor_v2a

The resulting output was copied below and modified appropriately. You'll have to do the following
manually to clean this up:
  * Rearrange models' order.
  * Make sure each model has one field with primary_key=True.
  * Make sure each ForeignKey has `on_delete` set to the desired behavior.
  * You can rename the models, but don't rename db_table.
  * If you rename a field, make sure there's a db_column value matching the original column name.

The models in this file have been aggressively trimmed of fields. If you need other data, they may
be available on the source tables for these models---you should check the source tables.
"""
import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta

from django.db import models
from django.db.utils import Error as DbError

from influencetx.core import constants, utils
from influencetx.tpj import models as tpj_models

log = logging.getLogger(__name__)

class Donor(models.Model):

    id = models.IntegerField(db_column='Ctrib_ID', primary_key=True)
    employer_id = models.IntegerField(db_column='Employer_ID', db_index=True,
                                      blank=True, null=True)

    full_name = models.CharField(db_column='FullName', max_length=150, blank=True, null=True)
    last_name = models.CharField(db_column='Surname', max_length=100, blank=True, null=True)
    first_name = models.CharField(db_column='FirstName', max_length=45, blank=True, null=True)
    suffix = models.CharField(db_column='Suffix', max_length=10, blank=True, null=True)
    title = models.CharField(max_length=160, blank=True, null=True)

    city = models.CharField(db_column='City', max_length=30, blank=True, null=True)
    state = models.CharField(db_column='StateAbbr', max_length=2, blank=True, null=True)
    zipcode = models.CharField(db_column='ZipCode', max_length=10, blank=True, null=True)
    zip = models.CharField(db_column='Zip', max_length=5, blank=True, null=True)
    city = models.CharField(db_column='CityPreferred', max_length=64, blank=True, null=True)

    employer = models.CharField(db_column='EMPLOYER', max_length=60, blank=True, null=True)
    occupation = models.CharField(db_column='Occupation', max_length=160, blank=True, null=True)
    interest_code = models.CharField(db_column='InterestCode', max_length=5)
    other_interests = models.CharField(db_column='OtherInterests', max_length=255,
                                       blank=True, null=True)

    total_contributions = models.DecimalField(db_column='CTRIB_AMT', max_digits=11, decimal_places=2, blank=True, null=True)

    party = models.CharField(db_column='Party', max_length=7, blank=True, null=True)
    politics = models.CharField(db_column='Politics', max_length=8000, blank=True, null=True)
    dem_score = models.SmallIntegerField(db_column='DemScore')

    class Meta:
        managed = False
        db_table = 'contributors'

#    def total_amounts(self, election_year=2016):
#        """Total Campaign contributions to legislators."""
#        if since is None:
#            since = datetime.now() - relativedelta(years=3)
#        contributions = tpj_models.Contribution.objects.filter(donor=self.id).filter(date__range=(since, datetime.now()))
#        contributions = tpj_models.Contribution.objects.filter(donor=self.id).filter(election_year=election_year)
#        total_amount = 0
#        for contrib in contributions:
#            total_amount += contrib.amount
#        return total_amount

    @utils.handle_error(DbError, lambda *args, **kwargs: [], log_level='warn')
    def contributions(self, max_count=20, election_year=2016):
        """Campaign contributions to legislators."""
#        if since is None:
#            since = datetime.now() - relativedelta(years=3)
#        contributions = tpj_models.Contribution.objects.filter(donor=self.id).filter(date__range=(since, datetime.now())).order_by('amount').reverse()[:max_count]
        contributions = tpj_models.Contribution.objects.filter(donor=self.id).filter(election_year=election_year).order_by('amount').reverse()[:max_count]
        return contributions


    def __str__(self):
        return self.full_name


class Filer(models.Model):

    id = models.IntegerField(db_column='iFILER_ID', primary_key=True)
    candidate_id = models.IntegerField(db_column='iCand_ID', blank=True, null=True, db_index=True)
    parent_candidate_id = models.IntegerField(
        db_column='iCand_Parent', blank=True, null=True,
        help_text='Parent id for deduped candidates. Matches candidate_id for non-dupes.',
    )

    title = models.CharField(max_length=15, blank=True, null=True)
    first_name = models.CharField(db_column='firstname', max_length=45, blank=True, null=True)
    last_name = models.CharField(db_column='surname', max_length=100, blank=True, null=True)
    suffix = models.CharField(max_length=5, blank=True, null=True)
    candidate_name = models.CharField(db_column='CandidateName', max_length=290,
                                      blank=True, null=True)

    city = models.CharField(max_length=30, blank=True, null=True)
    state = models.CharField(db_column='StateAbbr', max_length=2, blank=True, null=True)
    zipcode = models.CharField(db_column='Zipcode', max_length=10, blank=True, null=True)
    office = models.CharField(db_column='Office', max_length=100, blank=True, null=True)
    district = models.CharField(db_column='District', max_length=100, blank=True, null=True)

    party = models.CharField(db_column='Party', max_length=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'filers'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'.strip()


class Contribution(models.Model):
    id = models.IntegerField(db_column='IDNO', primary_key=True)
    donor = models.ForeignKey(Donor, db_column='ctrib_ID', blank=True, null=True)
    filer = models.ForeignKey(Filer, db_column='iFiler_ID', blank=True, null=True)
    amount = models.DecimalField(db_column='CTRIB_AMT', max_digits=19, decimal_places=2, blank=True, null=True)
    date = models.DateTimeField(db_column='CONT_DATE', blank=True, null=True)
    election_year = models.IntegerField(db_column='eYear', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contribs'

    def __str__(self):
        return f'{self.id} {self.amount}'
