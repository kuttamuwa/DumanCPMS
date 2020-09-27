from abc import ABC

from django.db import models

# Create your models here.
# dependent with CheckAccount application
from checkaccount.models import CheckAccount


class DataSetManager(models.Manager):
    @staticmethod
    def calc_period_day(period_velocity, **kwargs):
        if period_velocity is not None:
            return 30 // period_velocity
        else:
            last_twelve_month_avg_order_amount = kwargs.get('last_twelve_month_avg_order_amount')
            balance = kwargs.get('balance')

            if last_twelve_month_avg_order_amount is None or balance is None:
                raise ValueError("Vade hızı boş verilmiş. Hızın bulunması için gerekli diğer veriler olan son "
                                 "12 aylık ortalama sipariş tutarı ve bakiye bilgileri de eksik. \n"
                                 "Algoritmanın sağlıklı çalışabilmesi için ilgili verileri lütfen doldurun !")

            period_velocity = DataSetManager.calc_period_velocity(last_twelve_month_avg_order_amount, balance)

            return 30 // period_velocity

    @staticmethod
    def calc_period_velocity(last_twelve_month_avg_order_amount, balance):
        if balance is None:
            raise ValueError("Bakiye verisi doldurulmalı ! \n"
                             "Ozellikle devir gunu verilmediyse !")

        if last_twelve_month_avg_order_amount is None:
            raise ValueError("Bakiye verisi doldurulmalı ! \n"
                             "Ozellikle devir gunu verilmediyse !")

        return last_twelve_month_avg_order_amount // balance

    @staticmethod
    def calc_risk_excluded_warrant_balance(balance, warrant):
        if balance is None:
            raise ValueError("Bakiye verisi doldurulmalıdır ! \n"
                             "Ozellikle Bakiye harici risk verisi verilmediyse")

        if warrant is None:
            raise ValueError("Teminat verisi doldurulmalıdır ! \n"
                             "Ozellikle Bakiye harici risk verisi verilmediyse")

        return balance - warrant

    def save(self, *args, **kwargs):
        DataSetManager.save(*args, **kwargs)

    def create(self, *args, **kwargs):
        period_velocity = kwargs.get('period_velocity')
        period_day = kwargs.get('period_day')
        risk_excluded_warrant_balance = kwargs.get('risk_excluded_warrant_balance')
        warrant_state = kwargs.get('warrant_state')

        balance = kwargs['balance']
        warrant = kwargs['warrant']

        # last three months aberration
        # last three months payback comparison

        if warrant_state is None:
            # assigning default
            kwargs['warrant_amount'] = None

        if period_velocity is None:
            last_twelve_month_avg_order_amount = kwargs.get('last_twelve_month_avg_order_amount')
            balance = kwargs.get('balance')

            kwargs['period_velocity'] = DataSetManager.calc_period_velocity(last_twelve_month_avg_order_amount,
                                                                            balance)

        if period_day is None:
            kwargs['period_day'] = DataSetManager.calc_period_day(period_velocity, )

        if risk_excluded_warrant_balance is None:
            kwargs['risk_excluded_warrant_balance'] = DataSetManager.calc_risk_excluded_warrant_balance(balance,
                                                                                                        warrant)

        return super(DataSetManager, self).create(*args, **kwargs)


class DataSetModel(models.Model):
    objects = DataSetManager

    related_customer = models.ForeignKey(CheckAccount, on_delete=models.PROTECT)
    internal_customer_id = models.IntegerField(db_column='INTERNAL_CUSTOMER_ID', help_text='İç Müşteri Numarası',
                                               null=False)
    data_id = models.AutoField(primary_key=True)
    limit = models.PositiveIntegerField(db_column='LIMIT', null=False)  # 500 0000 vs
    warrant_state = models.BooleanField(db_column='WARRANT_STATE', help_text='teminat durumu',
                                        null=True, default=False)  # var yok
    warrant_amount = models.PositiveIntegerField(db_column='WARRANT_AMOUNT', help_text='teminat tutarı',
                                                 null=True)  # 500 000 vs
    maturity = models.IntegerField(db_column='MATURITY', help_text='vade günü', null=True)  # gun
    payment_frequency = models.PositiveSmallIntegerField(db_column='PAYMENT_FREQ',
                                                         help_text='odeme sikligi', null=True)  # 10, 5 gun
    maturity_exceed_avg = models.IntegerField(db_column='MATURITY_EXCEED_AVG',
                                              help_text='ortalama gecikme gun bakiyesi',
                                              null=True)  # gun
    avg_order_amount_last_twelve_months = models.FloatField(db_column='AVG_ORDER_AMOUNT_12',
                                                            help_text='Son 12 ay ortalama sipariş tutarı',
                                                            null=True)
    avg_order_amount_last_three_months = models.FloatField(db_column='AVG_ORDER_AMOUNT_3',
                                                           help_text='Son 3 ay ortalama sipariş tutarı',
                                                           null=True)
    last_3_months_aberration = models.PositiveSmallIntegerField(db_column='ABERRATION',
                                                                help_text="Son 3 ay ile son "
                                                                          "11 aylık satış ortalamasından sapma",
                                                                null=True)
    last_month_payback_perc = models.PositiveSmallIntegerField(db_column='PAYBACK_PERC_LAST',
                                                               help_text='Son ay iade yuzdesi',
                                                               null=True)
    last_twelve_months_payback_perc = models.FloatField(db_column='PAYBACK_PERC_12',
                                                        help_text='Son 12 ay iade yüzdesi',
                                                        null=True)
    avg_last_three_months_payback_perc = models.PositiveSmallIntegerField(db_column='AVG_PAYBACK_PERC_3',
                                                                          help_text='Son 3 ay iade yuzdesi', null=True)
    last_three_months_payback_comparison = models.SmallIntegerField(db_column='LAST_THREE_PAYBACK_COMP',
                                                                    help_text='Son 3 ay ile son 11 '
                                                                              'aylık iade %si karşılaştırması',
                                                                    null=True)
    avg_delay_time = models.SmallIntegerField(db_column='AVG_DELAY_TIME', help_text='Ort gecikme gun sayisi', null=True)
    avg_delay_balance = models.PositiveIntegerField(db_column='AVG_DELAY_BALANCE',
                                                    help_text='Ortalama gecikme gun bakiyesi', null=True)
    # calculated -> 30 / devir hizi
    period_day = models.PositiveIntegerField(db_column='PERIOD_DAY', help_text='Devir gunu', null=True)
    # calculated -> Musterinin aylik siparis hacmi / Musterinin aylik ortalama bakiyesi
    period_velocity = models.FloatField(db_column='PERIOD_VEL', help_text='Devir hizi', null=True)
    risk_excluded_warrant_balance = models.IntegerField(
        db_column='RISK_DIF_WARRANT_BALANCE',
        help_text='Teminat harici bakiye - risk', null=True)  # + - buyuk sayi calculated
    balance = models.PositiveIntegerField(db_column='BALANCE', help_text='Bakiye', null=True)
    profit = models.PositiveIntegerField(db_column='PROFIT', help_text='Kar', null=True)
    profit_percent = models.FloatField(db_column='PERC_PROFIT', help_text='Kar yuzdesi', null=True)
    total_risk_including_cheque = models.IntegerField(db_column='TOTAL_RISK_CHEQUE', help_text='Çek dahil toplam risk',
                                                      null=True)
    last_12_months_total_endorsement = models.PositiveIntegerField(db_column='LAST_12_TOTAL_ENDORSEMENT',
                                                                   help_text='Son 12 aylık toplam ciro',
                                                                   null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return CheckAccount.objects.get(customer_id=self.related_customer)

    class Meta:
        db_table = 'RISK_DATA'


class RiskDataSetPoints(models.Model):
    id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey(CheckAccount, on_delete=models.PROTECT)
    internal_customer_id = models.IntegerField(db_column='IC_MUSTERI_ID', null=False)
    son_12ay_ortalama_sapma_pts = models.PositiveSmallIntegerField(db_column='SON_SENE_ORT_SAPMA_PTS', null=True)
    kar_pts = models.PositiveSmallIntegerField(db_column='KAR_PTS', null=True)
    iade_pts = models.PositiveSmallIntegerField(db_column='IADE_PTS', null=True)
    ort_gecikme_pts = models.PositiveSmallIntegerField(db_column='ORT_GECIKME_PTS', null=True)
    ort_gecikme_gun_bakiyesi_pts = models.PositiveSmallIntegerField(db_column='ORT_GECIKME_GUN_BAKIYESI_PTS',
                                                                    null=True)
    devir_gunu_pts = models.PositiveSmallIntegerField(db_column='DEVIR_GUNU_PTS', null=True)
    teminatin_limit_riskini_karsilamasi_pts = models.PositiveSmallIntegerField(
        db_column='TEMINAT_LIMIT_RISK_KARSILASTIRMASI_PTS', null=True)

    class Meta:
        db_table = 'RISK_DATASET_POINTS'

    def __str__(self):
        return f'POINTS OF {self.internal_customer_id}'
