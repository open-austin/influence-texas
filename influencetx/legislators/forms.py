from django import forms

from . import models


class OpenStatesLegislatorForm(forms.ModelForm):

    class Meta:
        model = models.Legislator
        fields = ('first_name', 'last_name', 'middle_name', 'suffixes',
                  'party', 'district',
                  'openstates_updated_at', 'openstates_leg_id',
                  'transparencydata_id', 'votesmart_id',
                  'url', 'photo_url')
