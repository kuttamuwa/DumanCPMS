from django.db import models


class GeoModel(models.Model):
    objectid = models.AutoField(primary_key=True)

    def import_from_shapefile(self):
        pass

    def import_from_csv(self):
        pass

    class Meta:
        abstract = True

