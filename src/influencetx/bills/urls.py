from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        regex=r'^$',
        view=views.BillListView.as_view(),
        name='bill-list'
    ),
    url(
        regex=r'^(?P<pk>.+)/$',
        view=views.BillDetailView.as_view(),
        name='bill-detail'
    ),
]
