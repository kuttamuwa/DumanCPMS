from django.db import models

from risk_analysis.models import BaseModel, RiskDataSetPoints


class RiskDSAnalyze(BaseModel):
    risk_ds = models.ForeignKey(RiskDataSetPoints, on_delete=models.CASCADE, verbose_name='RISK_DS',
                                db_column='RISK_DS')
    general_point = models.FloatField(db_column='GENERAL_POINT')

    def __str__(self):
        return f'ANALYZE OF {self.risk_ds}'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(RiskDSAnalyze, self).save(force_insert, force_update, using, update_fields)

    class Meta:
        db_table = 'RISK_ANALYZE_POINTS'

    @staticmethod
    def import_all_riskdataset_into_analyze(default_point=0):
        for r in RiskDataSetPoints.objects.all():
            try:
                RiskDSAnalyze.objects.get(risk_ds=r)

            except RiskDSAnalyze.DoesNotExist:
                a = RiskDSAnalyze(risk_ds=r, general_point=default_point)
                a.save()
