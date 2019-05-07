from copy import deepcopy
import dateutil.parser
from django.db import transaction
from django.forms import ValidationError
from django.forms.models import model_to_dict
from slugify import slugify
from influencetx.core.constants import Vote
from influencetx.core.utils import party_enum
from influencetx.bills import forms, models
from influencetx.legislators.models import Legislator
from influencetx.legislators.forms import OpenStatesLegislatorForm
import logging
LOG = logging.getLogger(__name__)
DATETIME_TEMPLATE = '%Y-%m-%d %H:%M:%S'


def format_datetime(dt):
    """Return Open-States-style datetime string from datetime object."""
    return dt.strftime(DATETIME_TEMPLATE)


def parse_datetime(string):
    """Return datetime object from Open-States-style datetime string."""
    # FIXME: CT, CST don't seem to work here.
    return dateutil.parser.parse(string)


def adapt_openstates_legislator(api_data):
    """Return legislator data adapted to match Legislator model.
    Translate key names and casting data to match Legislator model.
    """
    adapted_data = deepcopy(api_data)
    # Update fields that require pre-processing before deserialization.
    adapted_data['openstates_leg_id'] = adapted_data['id']
    adapted_data['name'] = adapted_data['name']
    adapted_data['first_name'] = adapted_data['givenName']
    adapted_data['last_name'] = adapted_data['familyName']
    adapted_data['openstates_updated_at'] = parse_datetime(adapted_data['updatedAt'])
    adapted_data['party'] = party_enum(adapted_data['party'][0]['organization']['name']).value
    adapted_data['district'] = int(adapted_data['chamber'][0]['post']['label'])
    adapted_data['url'] = adapted_data['links'][0]['url']
    adapted_data['chamber'] = adapted_data['chamber'][0]['organization']['name']
    adapted_data['photo_url'] = adapted_data['image']

    return adapted_data


def deserialize_openstates_legislator(api_data, instance=None, commit=True):
    """Return Legislator model deserialized from Open States API data."""
    api_data = adapt_openstates_legislator(api_data)
    form = OpenStatesLegislatorForm(api_data, instance=instance)
    return clean_form(form, commit=commit)


def update_legislator_instance(instance, new_data, commit=True):
    """Update legislator instance with new data from Open States."""
    combined_data = model_to_dict(instance)
    combined_data.update(new_data)
    return deserialize_openstates_legislator(combined_data, instance=instance, commit=commit)


def find_matching_bill(openstates_bill_id):
    """Return Bill model matching Open States API data, if found in database."""
    # TODO: Add matching on official bill_id + session.
    return models.Bill.objects.filter(openstates_bill_id=openstates_bill_id).first()


def find_matching_vote_tally(data):
    """Return VoteTally model data adapted from Open States API, if found in database."""
    return models.VoteTally.objects.filter(openstates_vote_id=data['openstates_vote_id']).first()


def adapt_openstates_bill(api_data):
    """Return bill data adapted to match Bill model.
    Translate key names and casting data to match Bill model.
    """
    adapted_data = deepcopy(api_data)
    # Update fields that require pre-processing before deserialization.
    adapted_data['openstates_bill_id'] = adapted_data['id']
    adapted_data['bill_id'] = adapted_data['identifier']
    if len(adapted_data['versions']) > 0:
        last_version = adapted_data['versions'].pop()
        last_link = last_version['links'].pop()
        adapted_data['bill_text'] = last_link['url']
    else:
        adapted_data['bill_text'] = ""
    adapted_data['session'] = int(adapted_data['legislativeSession']['identifier'])
    adapted_data['chamber'] = adapted_data['fromOrganization']['name']
    adapted_data['subjects'] = adapted_data['subject']
    adapted_data['sponsors'] = [sponsor['name'] for sponsor in adapted_data['sponsorships']]
    adapted_data['openstates_updated_at'] = parse_datetime(adapted_data['updatedAt'])
    adapted_data['votes'] = adapted_data['votes']['edges']

    # TODO: Fix this once we get vote data
    # for vote_data in adapted_data['votes']:
    #     if vote_data['node']:
    #         adapt_openstates_vote_tally(vote_data['node'])

    return adapted_data


def adapt_openstates_vote_tally(vote_data):
    # TODO: Fix this once we get vote data
    """Adapt vote-tally data from Open States API to match VoteTally model.
    Unlike top-level adaptation functions, this modifies data in-place.
    """
    vote_data['openstates_vote_id'] = vote_data.pop('vote_id')
    vote_data['session'] = int(vote_data['session'])
    vote_data['date'] = parse_datetime(vote_data['date'])


@transaction.atomic
def deserialize_openstates_bill(api_data, instance=None):
    """Return Bill model deserialized from Open States API data."""
    adapted_data = adapt_openstates_bill(api_data)
    if instance is None:
        instance = find_matching_bill(adapted_data['openstates_bill_id'])
    # LOG.warn(f"Processing {adapted_data['bill_id']}")
    subject_models = deserialize_subject_tags(adapted_data.get('subjects', []))
    adapted_data['subjects'] = [s.id for s in subject_models]
    sponsor_models = deserialize_sponsor_names(adapted_data['chamber'], adapted_data.get('sponsors', []))
    adapted_data['sponsors'] = [l.id for l in sponsor_models]

    form = forms.OpenStatesBillForm(adapted_data, instance=instance)
    bill = clean_form(form, commit=True)

    actiondate_models = deserialize_action_dates(adapted_data.get('actions', []), bill)
    adapted_data['actions'] = [s.id for s in actiondate_models]
    # TODO: Fix this once we get vote data
    # for vote_data in adapted_data['votes']:
    #     vote_data['bill'] = bill.id
    #     deserialize_vote_tally(vote_data)
    return bill


def deserialize_subject_tags(subject_list):
    slug_list = [slugify(label, to_lower=True) for label in subject_list]
    return [
        models.SubjectTag.objects.get_or_create(slug=slug, defaults={'label': label})[0]
        for slug, label in zip(slug_list, subject_list)
    ]

def find_legislator_by_last_name(chamber, name):
    # LOG.warn(f"Finding Legislator: {name}, in {chamber}")
    try:
        legislator = Legislator.objects.get(
            chamber=chamber,
            last_name=name
        )
    except Legislator.DoesNotExist:
        try:
            legislator = Legislator.objects.get(
                chamber=chamber,
                name__contains=name
            )
        except:
            legislator = None
    except Legislator.MultipleObjectsReturned:
        legislator = None
        LOG.warn(f"too many: {name}, in {chamber}")
        
    return legislator


def find_legislator_by_full_name(chamber, name):
    try:
        legislator = Legislator.objects.get(
            chamber=chamber,
            name=name
        )
    except:
        legislator = None

    return legislator


def deserialize_sponsor_names(chamber, sponsor_names):
    """Find the legislator objects that match the names in sponsors"""
    model_list = []
    pattern = ','
    for aname in sponsor_names:
        # LOG.warn(f'Finding {aname}')
        if pattern in aname:
            """Name contains multiple elements"""
            name_array = aname.split(", ")
            first_part = name_array.pop()
            if first_part == 'Sr.' or first_part == 'Jr.':
                """Do search by last name"""
                last_name = name_array.pop()
                legislator = find_legislator_by_last_name(chamber, last_name)
            else:
                remaining_part = " ".join(name_array)
                combined_name = first_part + " " + remaining_part
                # LOG.warn(f'Finding combined_name {combined_name}')
                legislator = find_legislator_by_full_name(chamber, combined_name)
        else:
            legislator = find_legislator_by_last_name(chamber, aname)

        if legislator:
            model_list.append(legislator)
            # LOG.warn(f'Found sponsor {legislator}')
        else:
            print(f'Failed to find Legislator for sponsor name {aname}')

    return model_list


def deserialize_action_dates(action_list, instance):
    actiondate_models = []
    for action in action_list:
        if action:
            # LOG.warn(action)
            action_model, created = models.ActionDate.objects.get_or_create(
                bill=instance,
                date=action['date'],
                description=action['description'],
                classification=", ".join(action['classification']),
                # vote = action['vote'],
                order=action['order'],
            )
            # LOG.warn(action_model.id, created)
            actiondate_models.append(action_model)

    return actiondate_models


def deserialize_vote_tally(adapted_data, instance=None):
    # TODO: Fix this once we get vote data
    if instance is None:
        instance = find_matching_vote_tally(adapted_data)

    tally_form = forms.VoteTallyForm(adapted_data, instance=instance)
    tally = clean_form(tally_form, commit=True)

    deserialize_votes(adapted_data['yes_votes'], tally, vote_enum=Vote.YAY)
    deserialize_votes(adapted_data['no_votes'], tally, vote_enum=Vote.NAY)
    deserialize_votes(adapted_data['other_votes'], tally, vote_enum=Vote.OTHER)

    return tally


def deserialize_votes(vote_list, tally, vote_enum):
    # TODO: Fix this once we get vote data
    openstates_leg_ids = [vote['leg_id'] for vote in vote_list]
    individual_votes = []
    for leg_id in openstates_leg_ids:
        legislator = Legislator.objects.filter(openstates_leg_id=leg_id).first()
        if legislator:
            vote = models.SingleVote.objects.update_or_create(
                legislator=legislator,
                vote_tally=tally,
                defaults={'value': vote_enum.value},
            )
            individual_votes.append(vote)
        elif leg_id:
            LOG.warn(f"Legislator with openstates id {leg_id!r} not found.")
        else:
            LOG.debug(f"Vote has no associated leg_id.")
    return individual_votes


def clean_form(form, commit=True):
    if form.is_valid():
        return form.save(commit=commit)
    else:
        raise ValidationError(form.errors)
