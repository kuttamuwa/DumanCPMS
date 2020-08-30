from django.db import models

# Create your models here.
# dependent with CheckAccount application
from checkaccount.models import CheckAccount


class DataSetManager(models.Manager):
    def create(self, *args, **kwargs):
        period_velocity = kwargs.get('period_velocity')
        if period_velocity is None:
            last_twelve_month_avg_order_amount = kwargs.get('last_twelve_month_avg_order_amount')
            balance = kwargs.get('balance')

            kwargs['period_velocity'] = last_twelve_month_avg_order_amount // balance

        period_day = kwargs.get('period_day')
        if period_day is None:
            kwargs['period_day'] = 30 // period_velocity

        return super(DataSetManager, self).create(*args, **kwargs)


class DataSetModel(models.Model):
    objects = DataSetManager

    customer_id = models.ForeignKey(CheckAccount, on_delete=models.CASCADE)
    data_id = models.AutoField(primary_key=True)
    limit = models.PositiveIntegerField(db_column='LIMIT')  # 500 0000 vs
    warrant_state = models.BooleanField(db_column='WARRANT_STATE', help_text='teminat durumu')  # var yok
    warrant_amount = models.PositiveIntegerField(db_column='WARRANT_AMOUNT', help_text='teminat tutarı')  # 500 000 vs
    maturity = models.IntegerField(db_column='MATURITY', help_text='vade')  # gun
    payment_frequency = models.PositiveSmallIntegerField(db_column='PAYMENT_FREQ',
                                                         help_text='odeme sikligi')  # 10, 5 gun
    maturity_exceed_avg = models.IntegerField(db_column='MATURITY_EXCEED_AVG',
                                              help_text='ortalama gecikme gun bakiyesi')  # gun
    last_twelve_month_avg_order_amount = models.PositiveIntegerField(db_column='AVG_ORDER_AMOUNT',
                                                                     help_text='Son 12 ay ortalama sipariş tutarı')
    last_month_aberration = models.PositiveSmallIntegerField(db_column='ABERRATION',
                                                             help_text="Son 1 ay ile son "
                                                                       "11 aylık satış ortalamasından sapma")
    last_month_payback_perc = models.PositiveSmallIntegerField(db_column='PAYBACK_PERC',
                                                               help_text='Son ay iade yuzdesi')
    last_month_payback_comparison = models.SmallIntegerField(db_column='PAYBACK_COMP',
                                                             help_text='Son 1 ay ile son 11 '
                                                                       'aylık iade %si karşılaştırması')
    avg_delay_time = models.SmallIntegerField(db_column='AVG_DELAY_TIME', help_text='Ort gecikme gun sayisi')
    avg_delay_balance = models.PositiveIntegerField(db_column='AVG_DELAY_BALANCE',
                                                    help_text='Ortalama gecikme gun bakiyesi')
    period_day = models.PositiveIntegerField(db_column='PERIOD_DAY', help_text='Devir gunu')  # calculated
    period_velocity = models.PositiveSmallIntegerField(db_column='PERIOD_VEL', help_text='Devir hizi')  # calculated
    risk_excluded_warrant_balance = models.IntegerField(
        db_column='RISK_DIF_WARRANT_BALANCE',
        help_text='Teminat harici bakiye - risk')  # + - buyuk sayi calculated
    balance = models.PositiveIntegerField(db_column='BALANCE', help_text='Bakiye')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return CheckAccount.objects.get(customer_id=self.customer_id)
