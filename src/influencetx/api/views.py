from rest_framework import viewsets
from influencetx.users.models import User
from influencetx.tpj.models import Donor
from influencetx.bills.models import Bill
from influencetx.legislators.models import Legislator
from influencetx.api.serializers import UserSerializer, BillSerializer, LegislatorSerializer, DonorSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class LegislatorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Legislators to be viewed or edited.
    """
    queryset = Legislator.objects.all().order_by('name')
    serializer_class = LegislatorSerializer


class BillViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Bills to be viewed or edited.
    """
    queryset = Bill.objects.all().order_by('bill_id')
    serializer_class = BillSerializer


class DonorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Donors to be viewed or edited.
    """
    queryset = Donor.objects.all().order_by('id')
    serializer_class = DonorSerializer
