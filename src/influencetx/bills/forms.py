from django import forms

from . import models


class OpenStatesBillForm(forms.ModelForm):

    class Meta:
        model = models.Bill
        fields = ('title', 'session', 'chamber', 'subjects', 'sponsors', 'bill_text',
                  'bill_id', 'openstates_bill_id', 'openstates_updated_at')


class ActionDateForm(forms.ModelForm):

    class Meta:
        model = models.ActionDate
        fields = ('bill', 'date', 'description', 'classification', 'order')


class VoteTallyForm(forms.ModelForm):

    class Meta:
        model = models.VoteTally
        fields = ('bill', 'chamber', 'session', 'date',
                  'yes_count', 'no_count', 'other_count',
                  'passed', 'openstates_vote_id')
