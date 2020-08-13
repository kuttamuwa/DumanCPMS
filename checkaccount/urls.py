from django.urls import path

from checkaccount import views

urlpatterns = [
    path('api/', views.CheckAccountAPI.as_view())
]
