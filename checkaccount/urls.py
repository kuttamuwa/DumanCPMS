from django.contrib.auth.decorators import login_required
from django.urls import path

from checkaccount import views

urlpatterns = [
    # api
    path('api/get/', views.CheckAccountAPI.as_view()),

    path('testcustomer/<int:customer_id>', views.test_check_account_view),

    # pages and forms
    path('', views.checkaccount_mainpage),
    # path('checkaccount/retrieve', views.CheckAccountFormView.as_view(), name='checkaccount-retrieve'),
    path('retrieve/', views.NotImplementedPage, name='not-implemented-page'),
    path('create', views.CheckAccountFormCreateView.as_view(), name='checkaccount-create')
]

"""
search
Elasticsearch ile cebellesmemiz lazim..
"""
