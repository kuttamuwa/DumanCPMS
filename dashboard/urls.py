from django.urls import path, include

from dashboard import views

urlpatterns = [
    # path('', views.dashboard_with_pivot, name='dashboard_with_pivot'),
    # path('data', views.pivot_data, name='pivot_data'),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),

    path('data/', views.test_view),
    path('maps/', views.test_maps),
    path('notifications/', views.test_notifications),

    path('latest_accounts/<int:count>/', views.get_newest_check_accounts),

    path('', views.test_index)
]
