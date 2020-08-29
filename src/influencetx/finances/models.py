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
        return f"{self.elected_officer} - {self.year} - legID:{self.legislator_id}"


class Stock(models.Model):
    name = models.CharField(max_length=100)
    held_by = models.CharField(max_length=50,
                               choices=constants.HELD_BY_CHOICES)
    num_shares = models.CharField(max_length=100)
    financial_disclosure = models.ForeignKey(FinancialDisclosure,
                                             on_delete=models.CASCADE,
                                             related_name='stocks')

    def __str__(self):
        return f"{self.name} - finID:{self.financial_disclosure_id}"


class JobType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Job(models.Model):
    employer = models.CharField(max_length=100)
    held_by = models.CharField(max_length=50,
                               choices=constants.HELD_BY_CHOICES)
    position = models.CharField(max_length=100, blank=True)
    financial_disclosure = models.ForeignKey(FinancialDisclosure,
                                             on_delete=models.CASCADE,
                                             related_name='jobs')
    job_type = models.ForeignKey(JobType, on_delete=models.SET_NULL,
                                 blank=True, null=True, related_name='jobs')

    def legislator(self):
        return self.financial_disclosure.legislator.name

    def __str__(self):
        return f"{self.employer} - {self.position} - finID:{self.financial_disclosure_id}"


class Board(models.Model):
    name = models.CharField(max_length=100)
    held_by = models.CharField(max_length=50,
                               choices=constants.HELD_BY_CHOICES)
    position = models.CharField(max_length=100, blank=True)
    financial_disclosure = models.ForeignKey(FinancialDisclosure,
                                             on_delete=models.CASCADE,
                                             related_name='boards')

    def __str__(self):
        return f"{self.name} - {self.position} - finID:{self.financial_disclosure_id}"


class Gift(models.Model):
    donor = models.CharField(max_length=100)
    recipient = models.CharField(max_length=50,
                                 choices=constants.HELD_BY_CHOICES)
    description = models.CharField(max_length=100)
    financial_disclosure = models.ForeignKey(FinancialDisclosure,
                                             on_delete=models.CASCADE,
                                             related_name='gifts')

    def __str__(self):
        return f"{self.donor} - {self.description} - finID:{self.financial_disclosure_id}"
