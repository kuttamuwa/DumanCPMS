from django.urls import path, include
from django.views.generic import TemplateView

from dashboard import views
from dashboard.routers import router


urlpatterns = [

    # dashboard main page
    path('', views.DashBoardView.as_view(), name='dashboard-page'),

    # cruds
    path('api/limitexceeds/', views.LimitView.as_view(), name='limit-exceeds'),
    path('api/maturityexceeds/', views.MaturityView.as_view(), name='maturity-exceeds'),
    path('api/periodvelocity/', views.PeriodVelocityView.as_view(), name='period-velocity'),  # en kötü performans
    path('api/blacklist/<int:type>', views.BlackListView.as_view(), name='debts'),

    path('api/', include(router.urls), name='api-checkaccount'),
    path('index/', TemplateView.as_view(template_name='dboards/index.html'))




]
