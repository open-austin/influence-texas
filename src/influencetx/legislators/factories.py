from datetime import datetime

import factory

from . import models


class LegislatorFactory(factory.django.DjangoModelFactory):

    name = factory.Sequence(lambda n: 'first-{0} last-{0}'.format(n))
    first_name = factory.Sequence(lambda n: 'first-{0}'.format(n))
    last_name = factory.Sequence(lambda n: 'last-{0}'.format(n))

    party = 'I'
    chamber = 'lower'
    district = 1

    openstates_leg_id = 'ocd-person/51535358-7f46-4505-9a70-f7d611d33af2'
    openstates_updated_at = datetime.now()

    class Meta:
        model = models.Legislator
