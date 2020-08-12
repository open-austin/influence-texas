from django.conf.urls import url

from . import views

app_name = 'bills'
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
