from django.contrib import admin

# Register your models here.
from .models import CheckAccount, SysPersonnel, SysDepartments, PartnershipDocuments, Sectors


admin.site.register(CheckAccount)
admin.site.register(SysPersonnel)
admin.site.register(SysDepartments)
admin.site.register(PartnershipDocuments)
admin.site.register(Sectors)
