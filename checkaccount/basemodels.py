from django.db import models
from django.conf import settings


class BaseModel(models.Model):
    objects = models.Manager

    data_id = models.AutoField(primary_key=True)

    created_date = models.DateTimeField(auto_now_add=True, db_column='CREATED_DATE',
                                        name='Created Date')

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,
                                   on_delete=models.SET_NULL, name='Created by')

    class Meta:
        abstract = True
        db_table = 'BASEMODEL'


class GeoModel(BaseModel):
    name = models.CharField(max_length=50, db_column='NAME', unique=False)

    def import_from_shapefile(self):
        pass

    def import_from_csv(self):
        pass

    class Meta:
        abstract = True

    def __str__(self):
        return self.name
