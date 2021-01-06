from django.urls import path, include
from django.views.generic import TemplateView

from dashboard import views
from dashboard.routers import router


urlpatterns = [

    # dashboard main page
    path('', views.DashBoardView.as_view(), name='dashboard-page'),

    # path('api/', include(router.urls), name='api'),

    # Accounts
    path('accounts/', views.AccountAPIListView.as_view()),
    path('accounts/<int:pk>', views.AccountDetailView.as_view()),

    path('index/', TemplateView.as_view(template_name='dboards/index.html'))




]
