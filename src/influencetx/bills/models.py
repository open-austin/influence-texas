from django.db import models

from influencetx.core import constants
from influencetx.legislators.models import Legislator


class SubjectTag(models.Model):
    """A tag describing a subject-area for a bill."""

    label = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150)

    def __str__(self):
        return self.label


class Bill(models.Model):
    # Bill ID from Open States API.
    openstates_bill_id = models.CharField(max_length=48, db_index=True)
    # Official Bill ID.
    bill_id = models.CharField(max_length=10)
    title = models.TextField()
    bill_text = models.TextField(max_length=200, blank=True, null=True)
    session = models.IntegerField()
    chamber = models.CharField(max_length=6, choices=constants.CHAMBER_CHOICES)
    subjects = models.ManyToManyField(SubjectTag,
                                      blank=True,
                                      related_name='bills')
    sponsors = models.ManyToManyField(Legislator,
                                      blank=True,
                                      related_name='bills_sponsored')
    # updated_at field from Open States API. Used to check whether bill-detail needs update.
    openstates_updated_at = models.DateTimeField()

    def __str__(self):
        details = f'session: {self.session}, openstates_id: {self.openstates_bill_id}'
        return f'{self.bill_id} ({details})'


class ActionDate(models.Model):

    bill = models.ForeignKey(Bill,
                             on_delete=models.CASCADE,
                             related_name='action_dates')
    date = models.DateTimeField(blank=True, null=True)
    description = models.CharField(max_length=150, blank=True, null=True)
    classification = models.CharField(max_length=150, blank=True, null=True)
    # vote = models.OneToOneField(VoteTally, blank=True, null=True,
    #    on_delete=models.CASCADE, related_name='votes')
    order = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.order} {self.bill}'


class VoteTally(models.Model):
    """Result of a legislative vote on a bill."""

    bill = models.ForeignKey(Bill,
                             on_delete=models.CASCADE,
                             related_name='vote_results')
    chamber = models.CharField(max_length=6, choices=constants.CHAMBER_CHOICES)
    session = models.IntegerField()

    yes_count = models.IntegerField(default=0)
    no_count = models.IntegerField(default=0)
    other_count = models.IntegerField(default=0)

    passed = models.BooleanField()
    date = models.DateTimeField()

    openstates_vote_id = models.CharField(max_length=20, db_index=True)

    def is_null(self):
        return all(count == 0 for count in (self.yes_count, self.no_count,
                                            self.other_count))

    def __str__(self):
        return f'{self.bill}: yes={self.yes_count}, no={self.no_count}, other={self.other_count}'


class SingleVote(models.Model):
    """Single vote from from an individual legislator on an individual tally."""

    vote_tally = models.ForeignKey(VoteTally,
                                   on_delete=models.CASCADE,
                                   related_name='votes')
    legislator = models.ForeignKey(Legislator,
                                   on_delete=models.CASCADE,
                                   related_name='votes')
    value = models.CharField(max_length=1, choices=constants.VOTE_CHOICES)

    def __str__(self):
        return f'{self.legislator}, {self.vote_tally.bill}, vote={self.value}'
