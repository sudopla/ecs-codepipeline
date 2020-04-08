from django.conf.urls import url
from dashboard import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^aws$', views.AWSView.as_view(), name='aws'),
    url(r'^aws/storage$', views.get_aws_storage, name='aws_storage'),
    url(r'^aws/storage_monthly_usage$', views.get_aws_storage_monthly, name='aws_monthly_storage_usage'),
    url(r'^aws/monthly_costs$', views.get_aws_monthly_costs, name='aws_monthly_costs')
]

