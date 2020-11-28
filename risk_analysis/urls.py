from django.urls import path
from risk_analysis import views
from risk_analysis.filters import RiskAnalysisFilter, RiskPointsFilter, SGKDataFilter, TaxDataFilter

urlpatterns = [
    # create or import risk analysis dataset
    path('create/', views.creation_type_main_page, name='risk_analysis-create-page'),

    path('create/createoneform', views.CreateRiskAnalysisFormView.as_view(),
         name='risk_analysis-create-one'),

    path('create/importform', views.UploadRiskAnalysisDataView.as_view(),
         name='risk_analysis-upload'),

    # additional data: sgk
    path('create/importsgkdata', views.UploadSGKData.as_view(),
         name='risk_analysis-sgkupload'),
    path('retrieve/sgkdata', views.RetrieveSGKFormView.as_view(filterset_class=SGKDataFilter,
                                                               template_name='risk_analysis/sgk_data_retrieve.html')),

    # additional data : tax
    path('create/importtaxdata', views.UploadTaxData.as_view(),
         name='risk_analysis-taxupload'),
    path('retrieve/taxdata', views.RetrieveTaxFormView.as_view(filterset_class=TaxDataFilter,
                                                               template_name='risk_analysis/tax_data_retrieve.html')),

    # retrieving created risk analysis dataset
    path('retrieve/', views.RetrieveRiskAnalysisFormView.as_view(filterset_class=RiskAnalysisFilter,
                                                                 template_name=
                                                                 'risk_analysis/risk_analysis_retrieve.html'),
         name='risk_analysis-search'),


    path('points/', views.RetrieveRiskPointsFormView.as_view(filterset_class=RiskPointsFilter,
                                                             template_name='risk_analysis/risk_points_retrieve.html')),

    # general point of risk dataset
    path('analyzed/', views.RetrieveRiskDSAnalyze.as_view(), name='analyzed-index'),

    # main urls
    path('', views.risk_main_page),
    path('get/<int:customer_id>/', views.get_risk_by_customer_id,
         name='get-risk-data'),

    path('thanks/', views.generic_thanks),

]
