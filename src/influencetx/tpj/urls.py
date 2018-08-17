from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        regex=r'^$',
        view=views.DonorListView.as_view(),
        name='donor-list'
    ),
    url(
        regex=r'^donors/(?P<pk>\w+)/$',
        view=views.DonorDetailView.as_view(),
        name='donor-detail'
    ),
]
