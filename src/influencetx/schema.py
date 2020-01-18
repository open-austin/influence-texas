import graphene
from graphene import relay, Node
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from django.db import connection, transaction

from influencetx.legislators.models import Legislator, LegislatorIdMap
from influencetx.tpj.models import Donor, Contribution, Contributionsummary, Filer
from influencetx.bills.models import Bill, ActionDate, VoteTally, SingleVote, SubjectTag

import logging
log = logging.getLogger(__name__)

## default surprisingly does not have total count
class ExtendedConnection(graphene.Connection):
    class Meta:
        abstract = True

    total_count = graphene.Int()
    def resolve_total_count(self, info, **kwargs):
        return self.length

class BillType(DjangoObjectType):
    class Meta:
        model = Bill
        filter_fields = {
            'title': ['exact', 'icontains', 'istartswith'],
            'chamber': ['exact', 'icontains'],
        }
        interfaces = (relay.Node, )
        connection_class = ExtendedConnection
    pk = graphene.Int()
    def resolve_pk(self, info, **kwargs):
        return self.id


class DonorType(DjangoObjectType):
    class Meta:
        model = Donor
        filter_fields = {
            'id': ['exact', 'icontains', 'istartswith'],
            'full_name': ['exact', 'icontains'],
        }
        interfaces = (relay.Node, )
        connection_class = ExtendedConnection
    pk = graphene.Int()
    def resolve_pk(self, info, **kwargs):
        return self.id

class SubjectTagType(DjangoObjectType):
    class Meta:
        model = SubjectTag
        interfaces = (relay.Node, )
        connection_class = ExtendedConnection

class VoteTallyType(DjangoObjectType):
    class Meta:
        model = VoteTally
        interfaces = (relay.Node, )
        connection_class = ExtendedConnection


class ActionDateType(DjangoObjectType):
    class Meta:
        model = ActionDate
        interfaces = (relay.Node, )
        connection_class = ExtendedConnection

class SingleVoteType(DjangoObjectType):
    class Meta:
        model = SingleVote
        interfaces = (relay.Node, )
        connection_class = ExtendedConnection

class ContributionType(DjangoObjectType):
    class Meta:
        model = Contribution
        interfaces = (relay.Node, )
        connection_class = ExtendedConnection
        
class FilerType(DjangoObjectType):
    class Meta:
        model = Filer
        interfaces = (relay.Node, )
        connection_class = ExtendedConnection
    
    legislator = graphene.Field(lambda: LegislatorType)
    def resolve_legislator(self, info, **kwargs):
        try:
            id_map = LegislatorIdMap.objects.get(tpj_filer_id=self.id)
            return Legislator.objects.get(openstates_leg_id=id_map.openstates_leg_id)
        except LegislatorIdMap.DoesNotExist:
            log.warn(f"No linked legislator for {self.name}")

        return []

class ContributionsummaryType(DjangoObjectType):
    class Meta:
        model = Contributionsummary
        interfaces = (relay.Node, )
        connection_class = ExtendedConnection

    filer = graphene.Field(FilerType)
    def resolve_filer(self, info, **kwargs):
        return self.filer

class ClassificationCountType(graphene.ObjectType):
    count = graphene.Field(graphene.Int)
    classification = graphene.Field(graphene.String)
    average_order = graphene.Field(graphene.Float)

class ContributionssummaryTypeConnection(ExtendedConnection):
    class Meta:
        node = ContributionsummaryType

class LegislatorType(DjangoObjectType):
    class Meta:
        model = Legislator
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            'chamber': ['exact', 'icontains'],
            'party': ['exact', 'icontains'],
        }
        order_fields = ('name', 'name')
        interfaces = (relay.Node, )
        connection_class = ExtendedConnection

    pk = graphene.Int()
    def resolve_pk(self, info, **kwargs):
        return self.id
    
    contributions = relay.ConnectionField(ContributionssummaryTypeConnection)

    def resolve_contributions(self, info, **kwargs):
        try:
            id_map = LegislatorIdMap.objects.get(
                openstates_leg_id=self.openstates_leg_id)
            filer = Filer.objects.filter(id=id_map.tpj_filer_id).first()
            return Contributionsummary.objects.select_related(
                'donor').filter(filer=filer.id).order_by('-cycle_total')[:25]
        except LegislatorIdMap.DoesNotExist:
            log.warn(f"Filer id not found for openstates_leg_id {self.openstates_leg_id}" +
                    "in {LegislatorIdMap.objects.first}.")
        return []

def execute_raw_query(sql_string):
    cursor = connection.cursor()
    cursor.execute(sql_string)
    results = cursor.fetchall()
    list = []
    i = 0
    for row in results:
        dict = {} 
        field = 0
        while True:
            try:
                dict[cursor.description[field][0]] = str(results[i][field])
                field = field +1
            except IndexError as e:
                break
        i = i + 1
        list.append(dict) 
    return list


class Query(graphene.ObjectType):
    bill = graphene.Field(BillType, pk=graphene.Int())
    def resolve_bill(self, info, **kwargs):
        pk = kwargs.get('pk')
        return Bill.objects.get(pk=pk)

    bills = DjangoFilterConnectionField(BillType, classification=graphene.List(graphene.String))
    def resolve_bills(self, info, **kwargs):
        if kwargs.get("classification"):
            return Bill.objects.distinct().filter(action_dates__classification__in=kwargs.get("classification"))

        return Bill.objects.order_by("bill_id").all()

    bill_classification_stats = graphene.List(ClassificationCountType)
    def resolve_bill_classification_stats(self, info):
        return execute_raw_query("""
        SELECT classification, COUNT(classification), ROUND(AVG("order"),1) as average_order
        FROM bills_actiondate  a 
        WHERE a."order" = (SELECT MAX("order") FROM bills_actiondate c WHERE c.bill_id = a.bill_id AND c.classification != '' )
        GROUP BY(classification)
        ORDER BY average_order
        """)


    legislator = graphene.Field(LegislatorType, pk=graphene.Int())
    def resolve_legislator(self, info, **kwargs):
        pk = kwargs.get('pk')
        return Legislator.objects.get(pk=pk)

    legislators = DjangoFilterConnectionField(LegislatorType)
    def resolve_legislators(self, info, **kwargs):
        return Legislator.objects.all().order_by('district')

    donor = graphene.Field(DonorType, pk=graphene.Int())
    def resolve_donor(self, info, **kwargs):
        pk = kwargs.get('pk')
        return Donor.objects.get(pk=pk)

    donors = DjangoFilterConnectionField(DonorType)

schema = graphene.Schema(query=Query)
