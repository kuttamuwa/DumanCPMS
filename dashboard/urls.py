from django.urls import path, include

from dashboard import views

urlpatterns = [
    path('data/', views.test_view),
    path('maps/', views.test_maps),
    path('notifications/', views.test_notifications),

    path('latest_accounts/<int:count>/', views.get_newest_check_accounts),

    path('', views.test_index)
]
