from django.urls import path

from risk_analysis import views
from risk_analysis.filters import RiskAnalysisFilter, RiskPointsFilter, SGKDataFilter, TaxDataFilter

urlpatterns = [
    path('create/', views.creation_type_main_page, name='risk_analysis-create-page'),

    path('create/createoneform', views.CreateRiskAnalysisFormView.as_view(),
         name='risk_analysis-create-one'),

    path('create/importform', views.UploadRiskAnalysisDataView.as_view(),
         name='risk_analysis-upload'),

    path('create/importsgkdata', views.UploadSGKData.as_view(),
         name='risk_analysis-sgkupload'),

    path('create/importtaxdata', views.UploadTaxData.as_view(),
         name='risk_analysis-taxupload'),

    path('retrieve/', views.RetrieveRiskAnalysisFormView.as_view(filterset_class=RiskAnalysisFilter,
                                                                 template_name=
                                                                 'risk_analysis/risk_analysis_retrieve.html'),
         name='checkaccount-search'),

    path('retrieve/sgkdata', views.RetrieveSGKFormView.as_view(filterset_class=SGKDataFilter,
                                                               template_name='risk_analysis/sgk_data_retrieve.html')),

    path('retrieve/taxdata', views.RetrieveTaxFormView.as_view(filterset_class=TaxDataFilter,
                                                               template_name='risk_analysis/tax_data_retrieve.html')),

    path('points/', views.RetrieveRiskPointsFormView.as_view(filterset_class=RiskPointsFilter,
                                                             template_name='risk_analysis/risk_points_retrieve.html')),

    path('', views.risk_main_page),
    path('get/<int:customer_id>/', views.get_risk_by_customer_id,
         name='get-risk-data'),

]
