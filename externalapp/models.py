from django.db import models

# Create your models here.
from externalapp.basemodels import BaseModel


class BaseBlackLists(BaseModel):
    firm_name = models.CharField(max_length=150)

    def find_related_customers(self, customer):
        pass

    class Meta:
        db_table = 'BLACK_LIST'
        abstract = True

    def __str__(self):
        return 'Abstract Black List Object'


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


class ExternalBlackList(BaseBlackLists):
    class Meta:
        db_table = 'EXT_BLACK_LIST'

    def find_related_customers(self, customer):
        pass

    def __str__(self):
        return 'External Black List'


class SystemBlackList(BaseBlackLists):
    class Meta:
        db_table = 'SYS_BLACK_LIST'

    def find_related_customers(self, customer):
        pass

    def __str__(self):
        return 'System Black List'


class KonkordatoList(BaseBlackLists):
    class Meta:
        db_table = 'KONKORDATO_LIST'

    def find_related_customers(self, customer):
        pass

    def __str__(self):
        return 'Konkordato Black List'
