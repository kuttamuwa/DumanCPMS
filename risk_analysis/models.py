from django.conf import settings
from django.db import models

from checkaccount.models import CheckAccount, RelatedBlackList


# Create your models here.
# dependent with CheckAccount application
from risk_analysis.errors import MaturitySpeedError, BalanceError


class DataSetManager(models.Manager):
    @staticmethod
    def calc_period_day(period_velocity, **kwargs):
        if period_velocity is not None:
            return 30 // period_velocity
        else:
            last_twelve_month_avg_order_amount = kwargs.get('last_twelve_month_avg_order_amount')
            balance = kwargs.get('balance')

            if last_twelve_month_avg_order_amount is None or balance is None:
                raise MaturitySpeedError

            period_velocity = DataSetManager.calc_period_velocity(last_twelve_month_avg_order_amount, balance)

            return 30 // period_velocity

    @staticmethod
    def calc_period_velocity(last_twelve_month_avg_order_amount, balance):
        if balance is None:
            raise BalanceError

        if last_twelve_month_avg_order_amount is None:
            raise BalanceError

        return last_twelve_month_avg_order_amount // balance

    @staticmethod
    def calc_risk_excluded_warrant_balance(balance, warrant):
        if balance is None:
            raise BalanceError

        if warrant is None:
            raise BalanceError

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


class BaseModel(models.Model):
    objects = models.Manager

    data_id = models.AutoField(primary_key=True)

    created_date = models.DateTimeField(auto_now_add=True, db_column='CREATED_DATE',
                                        name='Created Date')

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,
                                   on_delete=models.SET_NULL, name='Created by')

    # edited_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'BASEMODEL'


class DataSetModel(BaseModel):
    # objects = DataSetManager

    related_customer = models.ForeignKey(CheckAccount, on_delete=models.PROTECT, verbose_name='İlişkili Müşteri',
                                         null=True)
    internal_customer_id = models.IntegerField(db_column='INTERNAL_CUSTOMER_ID', help_text='İç Müşteri Numarası',
                                               null=False, verbose_name='İç Müşteri No')

    limit = models.PositiveIntegerField(db_column='LIMIT', null=False, verbose_name='Limit')  # 500 0000 vs
    warrant_state = models.BooleanField(db_column='WARRANT_STATE', help_text='teminat durumu',
                                        null=True, default=False, verbose_name='Teminat Durumu')  # var yok
    warrant_amount = models.PositiveIntegerField(db_column='WARRANT_AMOUNT', help_text='teminat tutarı',
                                                 null=True, verbose_name='Teminat Tutarı')  # 500 000 vs
    maturity = models.IntegerField(db_column='MATURITY', help_text='vade günü', null=True,
                                   verbose_name='Vade Günü')  # gun
    payment_frequency = models.PositiveSmallIntegerField(db_column='PAYMENT_FREQ',
                                                         help_text='odeme sikligi', null=True,
                                                         verbose_name='Ödeme Sıklığı')  # 10, 5 gun
    maturity_exceed_avg = models.IntegerField(db_column='MATURITY_EXCEED_AVG',
                                              help_text='ortalama gecikme gun bakiyesi',
                                              verbose_name='Ortalama Gecikme Gün Bakiyesi',
                                              null=True)  # gun
    avg_order_amount_last_twelve_months = models.FloatField(db_column='AVG_ORDER_AMOUNT_12',
                                                            help_text='Son 12 ay ortalama sipariş tutarı',
                                                            null=True, verbose_name='Son 12 Ay Ortalama Sipariş Tutarı')
    avg_order_amount_last_three_months = models.FloatField(db_column='AVG_ORDER_AMOUNT_3',
                                                           help_text='Son 3 ay ortalama sipariş tutarı',
                                                           null=True, verbose_name='Son 3 Ay Ortalama Sipariş Tutarı')
    last_3_months_aberration = models.PositiveSmallIntegerField(db_column='ABERRATION',
                                                                help_text="Son 3 ay ile son "
                                                                          "11 aylık satış ortalamasından sapma",
                                                                null=True, verbose_name='Son 3 ay ile son 11 aylık '
                                                                                        'Satış ortalamasından sapma')
    # todo: üstteki hesaplanır:
    # todo: son 3 ay ile son 11 aylik satış ortalamasından sapma -> ((son 3 ay - son 12 ay) / son 12 ay) * 100

    last_month_payback_perc = models.PositiveSmallIntegerField(db_column='PAYBACK_PERC_LAST',
                                                               help_text='Son ay iade yuzdesi',
                                                               null=True, verbose_name='Son ay iade yüzdesi')
    last_twelve_months_payback_perc = models.FloatField(db_column='PAYBACK_PERC_12',
                                                        help_text='Son 12 ay iade yüzdesi',
                                                        null=True, verbose_name='Son 12 ay iade yüzdesi')
    last_three_months_payback_comparison = models.SmallIntegerField(db_column='LAST_THREE_PAYBACK_COMP',
                                                                    help_text='Son 3 ay ile son 11 '
                                                                              'aylık iade %si karşılaştırması',
                                                                    null=True, verbose_name='Son 3 ay ile son 11 '
                                                                                            'aylık iade yüzdesi '
                                                                                            'karşılaştırması')

    avg_last_three_months_payback_perc = models.PositiveSmallIntegerField(db_column='AVG_PAYBACK_PERC_3',
                                                                          help_text='Son 3 ay iade yuzdesi', null=True,
                                                                          verbose_name='Son 3 ay iade yüzdesi')

    # todo: last_three_months_payback_comparison = ((son 3 ay - son 12 ay) / son 12 ay) * 100

    avg_delay_time = models.SmallIntegerField(db_column='AVG_DELAY_TIME', help_text='Ort gecikme gun sayisi', null=True,
                                              verbose_name='Ortalama gecikme gün sayısı')
    avg_delay_balance = models.PositiveIntegerField(db_column='AVG_DELAY_BALANCE',
                                                    help_text='Ortalama gecikme gun bakiyesi', null=True,
                                                    verbose_name='Ortalama gecikme gün bakiyesi')
    # calculated -> 30 / devir hizi
    period_day = models.PositiveIntegerField(db_column='PERIOD_DAY', help_text='Devir gunu', null=True,
                                             verbose_name='Devir günü')
    # calculated -> Musterinin aylik siparis hacmi / Musterinin aylik ortalama bakiyesi
    period_velocity = models.FloatField(db_column='PERIOD_VEL', help_text='Devir hizi', null=True,
                                        verbose_name='Devir hızı')
    risk_excluded_warrant_balance = models.IntegerField(
        db_column='RISK_DIF_WARRANT_BALANCE',
        help_text='Teminat harici bakiye - risk', null=True, verbose_name='Teminat harici bakiye - risk')
    # + - buyuk sayi calculated

    # bakiye verisi yerine çek dahil toplam risk gelecek.
    balance = models.PositiveIntegerField(db_column='BALANCE', help_text='Bakiye', null=True, verbose_name='Bakiye')
    profit = models.PositiveIntegerField(db_column='PROFIT', help_text='Kar', null=True, verbose_name='Kar')
    profit_percent = models.FloatField(db_column='PERC_PROFIT', help_text='Kar yuzdesi', null=True,
                                       verbose_name='Kar yüzdesi')
    total_risk_including_cheque = models.IntegerField(db_column='TOTAL_RISK_CHEQUE', help_text='Çek dahil toplam risk',
                                                      null=True, verbose_name='Çek dahil toplam risk')
    last_12_months_total_endorsement = models.PositiveIntegerField(db_column='LAST_12_TOTAL_ENDORSEMENT',
                                                                   help_text='Son 12 aylık toplam ciro',
                                                                   null=True, verbose_name='Son 12 aylık toplam ciro')

    @classmethod
    def get_domain_list(cls):
        return [(i.name, i.verbose_name) for i in cls._meta.fields if i not in BaseModel._meta.fields
                and i.verbose_name not in ('basemodel ptr',)]

    def __str__(self):
        return CheckAccount.objects.get(customer_id=self.related_customer)

    class Meta:
        db_table = 'RISK_DATA'


class RiskDataSetPoints(BaseModel):
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


class SGKDebtListModel(BaseModel):
    taxpayer_number = models.CharField(unique=False, help_text='Sahis firmasi ise TCKNO, Tuzel Kisilik ise'
                                                               'Vergi No',
                                       db_column='TAXPAYER_NUMBER', max_length=15)
    firm_title = models.CharField(max_length=200, verbose_name='FIRM FULLNAME',
                                  db_column='FIRM_FULLNAME', unique=False)
    debt_amount = models.PositiveIntegerField(db_column='DEBT_AMOUNT', unique=False)

    class Meta:
        db_table = 'SGK_DEBTS'

    def __str__(self):
        return f"SGK Debts for {self.firm_title}"


class TaxDebtList(BaseModel):
    tax_department = models.CharField(max_length=200, verbose_name='TAX DEPARTMENT',
                                      db_column='TAX_DEPT', unique=False,
                                      help_text='Vergi Departmanı')
    taxpayer_number = models.CharField(unique=False, help_text='Sahis firmasi ise TCKNO, Tuzel Kisilik ise'
                                                               'Vergi No',
                                       db_column='TAXPAYER_NUMBER', max_length=15)
    dept_title = models.CharField(unique=False,
                                  help_text='Borçlunun Adı Soyadı/Unvanı',
                                  db_column='DEPT_TITLE', max_length=150)
    real_operating_income = models.CharField(unique=False,
                                             help_text='Esas Faaliyet Konusu',
                                             db_column='REAL_OPERATING_INCOME', max_length=500)
    dept_amount = models.FloatField(unique=False,
                                    help_text='Borç Miktarı',
                                    db_column='DEPT_AMOUNT')

    class Meta:
        db_table = 'TAX_DEBTS'

    def __str__(self):
        return f"Tax Debts for  {self.dept_title}"
