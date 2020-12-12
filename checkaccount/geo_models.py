from checkaccount.models import BaseModel
from django.db import models


class GeoModel(BaseModel):
    name = models.CharField(max_length=50, db_column='NAME', unique=True)

    def import_from_shapefile(self):
        pass

    def import_from_csv(self):
        pass

    class Meta:
        abstract = True

    def __str__(self):
        return self.name
