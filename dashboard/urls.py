from django.urls import path

from dashboard import views

urlpatterns = [
    path('data/', views.test_view),
    path('maps/', views.test_maps),
    path('notifications/', views.test_notifications),

    path('', views.test_index)
]