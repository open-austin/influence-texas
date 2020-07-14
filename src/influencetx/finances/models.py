from django.db import models
from influencetx.legislators.models import Legislator

class FinancialDisclosure(models.Model):
    year = models.CharField(max_length=4)
    elected_officer = models.CharField(max_length=100, blank=True)
    candidate = models.CharField(max_length=100, blank=True)
    legislator = models.ForeignKey(Legislator, on_delete=models.CASCADE, related_name='financial_disclosures')

    def __str__(self):
        return self.year + " - " + self.elected_officer
