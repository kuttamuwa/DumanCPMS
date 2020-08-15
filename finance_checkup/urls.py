from django.contrib.auth.decorators import login_required
from django.urls import path

from finance_checkup import views

urlpatterns = [
    path('', views.finance_checkup_page),

    # api
    # api guide
    path('api/', views.api_guide),

    # api arms
    path('api/risk_report/', views.RiskReportSummary.as_view()),
    path('api/check_report', views.CheckReportSummary.as_view()),
    path('api/guarantee_letter', views.GuaranteeLetterStateSummary.as_view()),
    path('api/findeks_risk_report', views.FindeksRiskReport.as_view())

    # site
    # todo ?
]

