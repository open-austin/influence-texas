from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        regex=r'^$',
        view=views.LegislatorListView.as_view(),
        name='legislator-list'
    ),
    url(
        regex=r'^legislators/(?P<pk>\w+)/$',
        view=views.LegislatorDetailView.as_view(),
        name='legislator-detail'
    ),
]
