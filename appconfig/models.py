from django.db import models

from checkaccount.models import CheckAccount
from risk_analysis.models import BaseModel


# Create your models here.
# Puantage #
class Domains(BaseModel):
    customer = models.ForeignKey(CheckAccount, on_delete=models.PROTECT,
                                 default=1)
    name = models.CharField(db_column='DOMAIN', max_length=100)
    point = models.FloatField(max_length=100, default=0.0, db_column='POINT',
                              help_text='Set your domain point of your variable'  # , validators=[validate_summary]
                              )

    @staticmethod
    def get_total_points():
        return sum(i.point for i in Domains.objects.all())

    def save(self, *args, **kwargs):
        if self.point + self.get_total_points() <= 100:
            super(Domains, self).save(*args, **kwargs)

        else:
            raise ValueError("Total of points exceeds 100")

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

    max_interval = models.FloatField(max_length=100, db_column='MAX_INTERVAL', help_text='Maximum interval')

    def save(self, *args, **kwargs):
        # total point control
        if self.pts is None:
            raise ValueError("Subtype point cannot be None !")

        if self.get_total_points(self.domain, self.pts) >= 100:
            raise ValueError(f"Point exceeds 100 for this domain : {self.domain}")

        # interval control
        # todo: bunu sonra cozecegim.

        super(Subtypes, self).save()

    @staticmethod
    def get_total_points(domain, pts):
        subtype_dom = Subtypes.objects.filter(domain=domain)
        if subtype_dom.__len__() != 0:
            s = sum(i.pts for i in Subtypes.objects.filter(domain=domain)) + pts
            return s
        else:
            return 0

    def __str__(self):
        return f"Points of {self.domain} : \n" \
               f"Minimum interval: {self.min_interval} \n" \
               f"Maximum interval: {self.max_interval}"

    class Meta:
        db_table = 'SUBTYPES'
