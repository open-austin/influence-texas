from datetime import datetime

import factory
from faker import Factory

from . import models


FAKE = Factory.create()


class BillFactory(factory.django.DjangoModelFactory):

    title = FAKE.pystr()
    chamber = 'lower'

    session = int(FAKE.pyint())

    bill_id = FAKE.pystr(max_chars=10)
    openstates_bill_id = FAKE.pystr()
    openstates_updated_at = datetime.now()

    class Meta:
        model = models.Bill
