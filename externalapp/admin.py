from django.contrib import admin

from externalapp.models import ExternalBlackList, KonkordatoList, SystemBlackList

# Register your models here.
admin.site.register(ExternalBlackList)
admin.site.register(KonkordatoList)
admin.site.register(SystemBlackList)