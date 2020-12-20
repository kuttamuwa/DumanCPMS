from django.urls import path

from risk_analysis import views
from risk_analysis.filters import RiskAnalysisFilter

urlpatterns = [
    # create or import risk analysis dataset
    path('create/', views.creation_type_main_page, name='risk_analysis-create-page'),

    path('create/createoneform', views.CreateRiskAnalysisFormView.as_view(),
         name='risk_analysis-create-one'),

    path('create/importform', views.UploadRiskAnalysisDataView.as_view(),
         name='risk_analysis-upload'),

    path('get/<int:pk>', views.RiskAnalysisDetailView.as_view(), name='get-riskds'),

    # retrieving created risk analysis dataset
    path('retrieve/', views.RiskAnalysisSearchView.as_view(
        filterset_class=RiskAnalysisFilter,
        template_name='risk_analysis/risk_analysis_retrieve.html'), name='risk_analysis-search'),

    path('analyze/<int:pk>', views.analyze_one, name='analyze-one'),

    # path('riskds/', views.RiskAnalysisSearchView.as_view(), name='riskds-list-analyze'),

    # main urls
    path('', views.risk_main_page, name='ra-index'),
    path('get/<int:customer_id>/', views.get_risk_by_customer_id,
         name='get-ca-risk-data'),

    path('thanks/', views.generic_thanks),

]
