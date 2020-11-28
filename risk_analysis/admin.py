from django.contrib import admin

# Register your models here.
from risk_analysis.models import DataSetModel, SGKDebtListModel, TaxDebtList

admin.site.register(DataSetModel)
admin.site.register(SGKDebtListModel)
admin.site.register(TaxDebtList)
