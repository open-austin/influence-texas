from django.db import models
from influencetx.legislators.models import Legislator
from influencetx.core import constants


class FinancialDisclosure(models.Model):
    year = models.CharField(max_length=4)
    elected_officer = models.CharField(max_length=100, blank=True)
    candidate = models.CharField(max_length=100, blank=True)
    legislator = models.ForeignKey(Legislator,
                                   on_delete=models.CASCADE,
                                   related_name='financial_disclosures')

    def __str__(self):
        return self.year + " - " + self.elected_officer


class Stocks(models.Model):
    name = models.CharField(max_length=100)
    held_by = models.CharField(max_length=50,
                               choices=constants.HELD_BY_CHOICES)
    num_shares = models.CharField(max_length=100)
    financial_disclosure = models.ForeignKey(FinancialDisclosure,
                                             on_delete=models.CASCADE,
                                             related_name='stocks')

    def __str__(self):
        return self.name


class Jobs(models.Model):
    employer = models.CharField(max_length=100)
    held_by = models.CharField(max_length=50,
                               choices=constants.HELD_BY_CHOICES)
    position = models.CharField(max_length=100, blank=True)
    financial_disclosure = models.ForeignKey(FinancialDisclosure,
                                             on_delete=models.CASCADE,
                                             related_name='jobs')


class Boards(models.Model):
    name = models.CharField(max_length=100)
    held_by = models.CharField(max_length=50,
                               choices=constants.HELD_BY_CHOICES)
    position = models.CharField(max_length=100, blank=True)
    financial_disclosure = models.ForeignKey(FinancialDisclosure,
                                             on_delete=models.CASCADE,
                                             related_name='boards')


class Gifts(models.Model):
    donor = models.CharField(max_length=100)
    recipient = models.CharField(max_length=50,
                                 choices=constants.HELD_BY_CHOICES)
    description = models.CharField(max_length=100)
    financial_disclosure = models.ForeignKey(FinancialDisclosure,
                                             on_delete=models.CASCADE,
                                             related_name='gifts')

    def __str__(self):
        return self.name
