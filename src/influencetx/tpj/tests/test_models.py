import factory.django
from factory import Faker

from influencetx.tpj import models


class DonorFactory(factory.django.DjangoModelFactory):

    full_name = Faker('name')

    class Meta:
        model = models.Donor


class FilerFactory(factory.django.DjangoModelFactory):

    first_name = Faker('first_name')
    last_name = Faker('last_name')

    class Meta:
        model = models.Filer


class ContributionFactory(factory.django.DjangoModelFactory):

    donor = factory.SubFactory(DonorFactory)
    filer = factory.SubFactory(FilerFactory)

    class Meta:
        model = models.Contribution


class TestDonor:

    def test_str(self):
        donor = DonorFactory.build()
        assert str(donor) == donor.full_name


class TestFiler:

    def test_str(self):
        filer = FilerFactory.build()
        assert str(filer) == f'{filer.first_name} {filer.last_name}'


class TestContribution:

    def test_str(self):
        contrib = ContributionFactory.build(amount=42)
        assert str(contrib) == f'{contrib.donor!r} {contrib.filer!r} {contrib.amount} '
