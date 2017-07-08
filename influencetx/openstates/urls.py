from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        regex=r'^$',
        view=views.IndexView.as_view(),
        name='index'
    ),
    url(
        regex=r'^legislators/$',
        view=views.LegislatorListView.as_view(),
        name='legislator-list'
    ),
    url(
        regex=r'^legislators/(?P<leg_id>\w+)/$',
        view=views.LegislatorDetailView.as_view(),
        name='legislator-detail'
    ),
    url(
        regex=r'^bills/$',
        view=views.BillListView.as_view(),
        name='bill-list'
    ),
    url(
        regex=r'^bills/(?P<session>\d+)/(?P<id>.+)/$',
        view=views.BillDetailView.as_view(),
        name='bill-detail'
    ),
    url(
        regex=r'^api_key_required/$',
        view=views.APIKeyRequiredView.as_view(),
        name='api-key-required'
    ),
]
