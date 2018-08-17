from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        regex=r'^$',
        view=views.LegislatorListView.as_view(),
        name='legislator-list'
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
