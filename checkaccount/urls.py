from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path

from DumanCPMS import settings
from checkaccount import views
from checkaccount.filters import CheckAccountFilter
from checkaccount.views import CheckAccountSearchView

urlpatterns = [
    # api
    path('api/get/', views.CheckAccountAPI.as_view()),

    # pages and forms
    path('', views.checkaccount_mainpage),
    path('retrieve/', CheckAccountSearchView.as_view(filterset_class=CheckAccountFilter,
                                                     template_name='checkaccount/checkaccount_retrieve.html'),
         name='checkaccount-search'),

    path('create/', views.CheckAccountFormCreateView.as_view(),
         name='checkaccount-create'),

    path('get/<int:customer_id>/<int:state>', views.get_customer),
    path('get/<int:customer_id>/', views.get_customer),

    # upload files
    path('get/<int:customer_id>/upload', views.UploadAccountDocumentsView.as_view(), name='upload_docs'),

    path('get/<int:customer_id>/docs', views.GetAccountDocumentsList.as_view(), name='docs'),

    path('get/<int:pk>/<int:type>/docs/delete', views.DeleteAccountDocumentsView.as_view(), name='delete_docs'),

    path('get/<pk>/delete', views.CheckAccountFormDeleteView.as_view(), name='delete_customer'),

    path('succeed/', views.succeed_create_check_account),
    path('docs/delete/succeed/', views.delete_succeed_doc),

    path('loginapp/', auth_views.LoginView.as_view(), name='app-login'),
]
