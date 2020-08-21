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
                                                     template_name='checkaccount/checkaccount_retrieve.html'),
         name='checkaccount-search'),

    path('create/', views.CheckAccountFormCreateView.as_view(),
         name='checkaccount-create'),

    path('get/<int:customer_id>/<str:state>', views.get_customer),
    path('get/<int:customer_id>/', views.get_customer),

    path('succeed/', views.succeed_create_check_account),
    path('loginapp/', auth_views.LoginView.as_view(), name='app-login'),

    # attachment
    # path('attach/<int:customer_id>', views),

]

"""
search
Elasticsearch ile cebellesmemiz lazim..
"""
