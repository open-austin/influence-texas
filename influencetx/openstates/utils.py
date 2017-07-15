from datetime import datetime

from django.forms import ValidationError
from django.forms.models import model_to_dict

from influencetx.core.utils import party_enum
from influencetx.legislators import forms


DATETIME_TEMPLATE = '%Y-%m-%d %H:%M:%S'


def format_datetime(dt):
    """Return Open-States-style datetime string from datetime object."""
    return dt.strftime(DATETIME_TEMPLATE)


def parse_datetime(string):
    """Return datetime object from Open-States-style datetime string."""
    return datetime.strptime(string, DATETIME_TEMPLATE)


def adapt_openstates_legislator(json_data):
    """Return legislator data adapted to match Legislator model.

    This pre-processs data by translating key names and casting data to match Legislator model.
    """
    json_data = json_data.copy()  # Copy data to avoid side-effects (data modified below).

    # Update fields that require pre-processing before deserialization.
    updated_at = json_data.pop('updated_at')
    json_data['openstates_updated_at'] = parse_datetime(updated_at)
    json_data['openstates_leg_id'] = json_data.pop('leg_id')
    json_data['party'] = party_enum(json_data.get('party')).value

    return json_data


def deserialize_openstates_legislator(json_data, instance=None, commit=True):
    """Return Legislator model deserialized from Open States API data."""
    json_data = adapt_openstates_legislator(json_data)
    form = forms.OpenStatesLegislatorForm(json_data, instance=instance)

    if form.is_valid():
        return form.save(commit=commit)
    else:
        raise ValidationError(form.errors)


def update_legislator_instance(instance, new_data, commit=True):
    """Update legislator instance with new data from Open States."""
    combined_data = model_to_dict(instance)
    combined_data.update(new_data)
    return deserialize_openstates_legislator(combined_data, instance=instance, commit=commit)
