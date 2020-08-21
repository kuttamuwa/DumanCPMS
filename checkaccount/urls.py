from django.urls import path
from django.contrib.auth import views as auth_views
from django_filters.views import FilterView

from checkaccount import views
from checkaccount.filters import CheckAccountFilter
from checkaccount.views import CheckAccountSearchView

urlpatterns = [
    # api
    path('api/get/', views.CheckAccountAPI.as_view()),

    # pages and forms
    path('', views.checkaccount_mainpage),
    path('retrieve/', CheckAccountSearchView.as_view(filterset_class=CheckAccountFilter,
                                                     template_name='checkaccount/account_with_filter.html'),
         name='checkaccount-search'),

    path('create/', views.CheckAccountFormCreateView.as_view(success_url='/checkaccount/succeed'),
         name='checkaccount-create'),

    # path('attachmentest/', views.upload_file),
    path('get/<int:customer_id>', views.get_customer),

    path('succeed/', views.succeed_create_check_account),
    path('loginapp/', auth_views.LoginView.as_view(), name='app-login')
]

"""
search
Elasticsearch ile cebellesmemiz lazim..
"""
