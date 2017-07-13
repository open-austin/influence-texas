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


def deserialize_openstates_legislator(json_data):
    """Return Legislator model deserialized from Open States API data."""
    json_data = json_data.copy()  #
    json_data['party'] = party_enum(json_data['party']).value

    updated_at = json_data.pop('updated_at')
    json_data['openstates_updated_at'] = parse_datetime(updated_at)
    json_data['openstates_leg_id'] = json_data.pop('leg_id')

    form = forms.OpenStatesLegislatorForm(json_data)

    if form.is_valid():
        return form.save()
    else:
        raise ValidationError(form.errors)
