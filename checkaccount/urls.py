from django.contrib.auth.decorators import login_required
from django.urls import path

from checkaccount import views

urlpatterns = [
    path('', views.main_page),

    # api
    path('api/checkaccount/', views.CheckAccountAPI.as_view()),

    # pages and forms
    # path('checkaccount/add/', views.CheckAccountFormCreateView.as_view(), name='checkaccount-add'),

    path('checkaccount/', views.CheckAccountFormCreateView.as_view(), name='checkaccount-create')
]
