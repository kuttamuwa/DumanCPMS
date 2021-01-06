from django.contrib.auth import views as auth_views
from django.urls import path, include

from checkaccount import views
from checkaccount.routers import router
from checkaccount.filters import CheckAccountFilter
from checkaccount.views import CheckAccountSearchView

urlpatterns = [
    # pages and forms
    path('', views.checkaccount_mainpage, name='ch-index'),
    path('retrieve/', CheckAccountSearchView.as_view(filterset_class=CheckAccountFilter,
                                                     template_name='checkaccount/checkaccount_retrieve.html'),
         name='checkaccount-search'),

    path('create/', views.CheckAccountFormCreateView.as_view(),
         name='checkaccount-create'),

    path('get/<int:pk>/', views.CheckAccountView.as_view(), name='get_customer'),  #

    # upload files
    path('get/<int:pk>/upload', views.UploadAccountDocumentsView.as_view(), name='upload_docs'),  # pk: check account

    path('get/<int:pk>/docs', views.GetAccountDocumentsList.as_view(), name='docs'),  # pk: check account pk

    path('get/<int:pk>/<int:type>/docs/delete',
         views.DeleteAccountDocumentsView.as_view(), name='delete_docs'),  # pk: acc

    path('get/<int:pk>/delete', views.CheckAccountFormDeleteView.as_view(), name='delete_customer'),  # pk: ca

    path('succeed/', views.succeed_create_check_account),
    path('docs/delete/succeed/', views.delete_succeed_doc),

    path('loginapp/', auth_views.LoginView.as_view(), name='app-login'),

    # crud - api
    path('api/', include(router.urls))
]
