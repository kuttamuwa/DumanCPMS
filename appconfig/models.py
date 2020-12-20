from django.db import models

from appconfig.errors import DomainPointsValueError
from risk_analysis.models import BaseModel
import numpy as np


# Create your models here.
# Puantage #
class Domains(BaseModel):
    name = models.CharField(db_column='DOMAIN', max_length=100)
    point = models.FloatField(max_length=100, default=0.0, db_column='POINT',
                              help_text='Set your domain point of your variable'  # , validators=[validate_summary]
                              )

    @staticmethod
    def get_total_points(alert=False):
        sum_pts = [i['point'] for i in Domains.objects.values('point')]
        if alert:
            if sum_pts != 100:
                DomainPointsValueError()

    def save(self, *args, **kwargs):
        super(Domains, self).save(*args, **kwargs)

    def __str__(self):
        return f'Domain: {self.name} \n' \
               f'General Point : {self.point}'

    class Meta:
        db_table = 'DOMAINS'


class Subtypes(BaseModel):
    domain = models.ForeignKey(Domains, on_delete=models.PROTECT, max_length=100)

    pts = models.FloatField(max_length=100, db_column='PTS', help_text='Point of specified intervals '
                                                                       'of your subtype related Domain')
    min_interval = models.FloatField(max_length=100, db_column='MIN_INTERVAL', help_text='Minimum interval')

    max_interval = models.FloatField(max_length=100, db_column='MAX_INTERVAL', help_text='Maximum interval',
                                     blank=True, null=True)

    def save(self, *args, **kwargs):
        # total point control
        if not self.pts + self.get_total_points(self.domain) <= 100:
            raise DomainPointsValueError

        if self.max_interval is None:
            self.max_interval = np.inf

        # interval control
        # todo: bunu sonra cozecegim.

        super(Subtypes, self).save()

    @staticmethod
    def get_total_points(domain):
        return sum(i.pts for i in Subtypes.objects.filter(domain=domain))

    def __str__(self):
        return f"Points of {self.domain} : \n" \
               f"Minimum interval: {self.min_interval} \n" \
               f"Maximum interval: {self.max_interval}"

    class Meta:
        db_table = 'SUBTYPES'
