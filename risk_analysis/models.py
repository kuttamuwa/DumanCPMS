from django.db import models

# Create your models here.
# dependent with CheckAccount application
from checkaccount.models import CheckAccount


class DataSetManager(models.Manager):
    def create(self, *args, **kwargs):
        # todo:  hesaplamalar girer
        if kwargs.get('period_day') is None:
            period_day = kwargs.get()
        return super(DataSetManager, self).create(*args, **kwargs)


class DataSetModel(models.Model):
    objects = DataSetManager

    customer_id = models.ForeignKey(CheckAccount, on_delete=models.CASCADE)
    data_id = models.AutoField(primary_key=True)
    limit = models.PositiveIntegerField(db_column='LIMIT')  # 500 0000 vs
    warrant_state = models.BooleanField(db_column='WARRANT_STATE')  # var yok
    warrant_amount = models.PositiveIntegerField(db_column='WARRANT_AMOUNT')  # 500 000 vs
    maturity = models.IntegerField(db_column='MATURITY')  # gun
    maturity_exceed_avg = models.IntegerField(db_column='MATURITY_EXCEED_AVG')  # gun
    payment_frequency = models.PositiveSmallIntegerField(db_column='PAYMENT_FREQ')  # 10, 5 gun
    last_twelve_month_avg_order_amount = models.PositiveIntegerField(db_column='AVG_ORDER_AMOUNT')
    last_month_aberration = models.PositiveSmallIntegerField(db_column='ABERRATION')
    last_month_payback_perc = models.PositiveSmallIntegerField(db_column='PAYBACK_PERC')
    last_month_payback_comparison = models.SmallIntegerField(db_column='PAYBACK_COMP')
    avg_delay_time = models.SmallIntegerField(db_column='AVG_DELAY_TIME')
    avg_delay_balance = models.PositiveIntegerField(db_column='AVG_DELAY_BALANCE')
    period_day = models.PositiveIntegerField(db_column='PERIOD_DAY')  # calculated
    period_velocity = models.PositiveSmallIntegerField(db_column='PERIOD_VEL')  # calculated
    risk_excluded_warrant_balance = models.IntegerField(
        db_column='RISK_DIF_WARRANT_BALANCE')  # + - buyuk sayi calculated
    bakiye = models.PositiveIntegerField(db_column='BALANCE')

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return CheckAccount.objects.get(customer_id=self.customer_id)
