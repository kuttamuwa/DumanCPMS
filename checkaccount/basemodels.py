from django.db import models
from django.conf import settings


class BaseManager(models.Manager):
    pass


class BaseModel(models.Model):
    # objects = BaseManager

    data_id = models.AutoField(primary_key=True)

    created_date = models.DateTimeField(auto_now_add=True, db_column='CREATED_DATE',
                                        verbose_name='Created Date')

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,
                                   on_delete=models.SET_NULL, verbose_name='Created by')

    class Meta:
        abstract = True
        db_table = 'BASEMODEL'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.created_by is None:
            pass

        super(BaseModel, self).save(force_insert, force_update, using, update_fields)


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
