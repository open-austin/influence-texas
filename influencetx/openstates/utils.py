from datetime import datetime

from django.forms import ValidationError

from influencetx.core.utils import party_enum
from influencetx.legislators import forms


DATETIME_TEMPLATE = '%Y-%m-%d %H:%M:%S'


def format_datetime(dt):
    """Return Open-States-style datetime string from datetime object."""
    return dt.strftime(DATETIME_TEMPLATE)


def parse_datetime(string):
    """Return datetime object from Open-States-style datetime string."""
    return datetime.strptime(string, DATETIME_TEMPLATE)


def deserialize_openstates_legislator(json_data, commit=True):
    """Return Legislator model deserialized from Open States API data."""
    json_data = json_data.copy()  # Copy data to avoid side-effects (data modified below).

    # Update fields that require pre-processing before deserialization.
    updated_at = json_data.pop('updated_at')
    json_data['openstates_updated_at'] = parse_datetime(updated_at)
    json_data['openstates_leg_id'] = json_data.pop('leg_id')
    json_data['party'] = party_enum(json_data.get('party')).value

    form = forms.OpenStatesLegislatorForm(json_data)

    if form.is_valid():
        return form.save(commit=commit)
    else:
        raise ValidationError(form.errors)
