from django.urls import path
from externalapp.views import UploadExternalBlackListView, UploadSystemBlackListView
from externalapp.views import UploadSGKDebtView, UploadKonkordatoView
from externalapp.views import UploadTAXDebtView

urlpatterns = [

    path('upload/extblacklist', UploadExternalBlackListView.as_view(), name='upload-extblacklist'),
    path('upload/extsysblacklist', UploadSystemBlackListView.as_view(), name='upload-sysblacklist'),
    path('upload/sgkdebtlist', UploadSGKDebtView.as_view(), name='upload-sgkdebtlist'),
    path('upload/konkordatolist', UploadKonkordatoView.as_view(), name='upload-konkordatolist'),
    path('upload/taxdebtlist', UploadTAXDebtView.as_view(), name='upload-taxdebtlist'),

    path('get/extblacklist', name='get-extblacklist'),
    path('get/sysblacklist', name='get-sysblacklist'),

    path('get/konkordatolist', name='get-konkordatolist'),
    path('get/taxdebtlist', name='get-taxdebtlist'),
    path('get/sgkdebtlist', name='get-sgkdebtlist'),

]
