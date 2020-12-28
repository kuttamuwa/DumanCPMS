from django.urls import path, include

from dashboard import views

urlpatterns = [
    path('get/limitexceeds/', views.AccountInitialProcesses().limitexceeds, name='limit-exceeds'),

]
