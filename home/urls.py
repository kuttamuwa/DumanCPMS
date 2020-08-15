from django.contrib.auth.decorators import login_required
from django.urls import path

from home import views

urlpatterns = [
    path('', views.main_page),
    path('contact/', views.contact_page),
]
