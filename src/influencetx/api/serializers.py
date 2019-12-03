from influencetx.users.models import User
from influencetx.tpj.models import Donor
from influencetx.legislators.models import Legislator
from influencetx.bills.models import Bill
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'name', 'email', 'groups']


class LegislatorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Legislator
        fields = ['url', 'name', 'chamber', 'district', 'party', 'photo_url']


class BillSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Bill
        fields = ['bill_id', 'title', 'chamber', 'session']


class DonorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Donor
        fields = ['full_name', 'city', 'zipcode', 'employer', 'occupation']
