from django.urls import path
from django.contrib.auth import views as auth_views
from checkaccount import views

urlpatterns = [
    # api
    path('api/get/', views.CheckAccountAPI.as_view()),

    # pages and forms
    path('', views.checkaccount_mainpage),
    # path('checkaccount/retrieve', views.CheckAccountFormView.as_view(), name='checkaccount-retrieve'),
    path('retrieve/', views.check_account_search, name='checkaccount-retrieve'),
    path('create/', views.CheckAccountFormCreateView.as_view(success_url='/checkaccount/succeed'),
         name='checkaccount-create'),

    path('succeed/', views.succeed_create_check_account),
    path('loginapp/', auth_views.LoginView.as_view(), name='app-login')
]

"""
search
Elasticsearch ile cebellesmemiz lazim..
"""
