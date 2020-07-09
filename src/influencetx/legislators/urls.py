from django.conf.urls import url

from . import views

app_name = 'legislators'
urlpatterns = [
    url(
        regex=r'^$',
        view=views.LegislatorListView.as_view(),
        name='legislator-list'
    ),
    url(
        regex=r'^findreps/(?P<pk_s>[0-9]+),(?P<pk_h>[0-9]+)$',
        view=views.FindrepsListView.as_view(),
        name='findreps-list'
    ),
    url(
        regex=r'^senators$',
        view=views.SenatorListView.as_view(),
        name='senator-list'
    ),
    url(
        regex=r'^representatives$',
        view=views.RepresentativeListView.as_view(),
        name='representative-list'
    ),
    url(
        regex=r'^legislators/(?P<pk>\w+)/$',
        view=views.LegislatorDetailView.as_view(),
        name='legislator-detail'
    ),
]
