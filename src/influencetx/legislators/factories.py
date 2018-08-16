from datetime import datetime

import factory

from . import models


class LegislatorFactory(factory.django.DjangoModelFactory):

    first_name = factory.Sequence(lambda n: 'first-{0}'.format(n))
    last_name = factory.Sequence(lambda n: 'last-{0}'.format(n))
    middle_name = factory.Sequence(lambda n: 'middle-{0}'.format(n))

    party = 'I'
    chamber = 'lower'
    district = 1

    openstates_leg_id = 'TXL000000'
    openstates_updated_at = datetime.now()

    class Meta:
        model = models.Legislator
