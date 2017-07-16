from django import forms

from . import models


class OpenStatesBillForm(forms.ModelForm):

    class Meta:
        model = models.Bill
        fields = ('title', 'session',
                  'bill_id', 'openstates_bill_id', 'openstates_updated_at')


class ActionDatesForm(forms.ModelForm):

    class Meta:
        model = models.ActionDates
        fields = ('bill', 'first', 'last', 'passed_lower', 'passed_upper', 'signed')


class VoteTallyForm(forms.ModelForm):

    class Meta:
        model = models.VoteTally
        fields = ('bill', 'chamber', 'session', 'date',
                  'yes_count', 'no_count', 'other_count',
                  'passed', 'openstates_vote_id')
