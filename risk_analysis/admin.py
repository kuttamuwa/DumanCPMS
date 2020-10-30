from django.contrib import admin

# Register your models here.
from risk_analysis.models import Domains, Subtypes, BaseModel

admin.site.register(Domains)
admin.site.register(Subtypes)
admin.site.register(BaseModel)