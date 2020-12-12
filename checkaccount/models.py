from django.contrib.auth.models import User
from django.db import models

from .errors import SoleTraderMustHaveTaxPayerNumber, LegalEntityMustHaveBirthPlace
from .fields import DumanModelFileField
from .geo_models import GeoModel
from .model_sys_specs import CariHesapSpecs, AccountDocumentsSpec, PartnershipDocumentsSpecs
import os
from django.conf import settings

"""
UYARILAR:
Firmaya özel Kara liste, geçmiş kara listesi aktarılır
Vergi borcu olanlar listeden uyarı
SGK borcu olanlar listeden uyarı
Sistemdeki tüm kullanıcıların verisine dayalı kara liste uygulaması
Konkordato listesi alınabilir mi

Müşteri çekilirken kayıt sayısı sistemdeki ile uyuşmazsa hata verir

"""


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


class CheckAccountManager(models.Manager):
    def create(self, *args, **kwargs):
        return super(CheckAccountManager, self).create(*args, **kwargs)


class Cities(GeoModel):
    city_plate_number = models.PositiveSmallIntegerField(db_column='CITY_PLATE_NUMBER', unique=True, db_index=True)

    def import_from_shapefile(self):
        pass

    def import_from_csv(self):
        pass

    class Meta:
        db_table = 'CITIES'
        indexes = [
            models.Index(fields=['city_name'])
        ]


class Districts(GeoModel):
    city = models.ManyToOneRel(Cities, on_delete=models.CASCADE)

    def import_from_shapefile(self):
        pass

    def import_from_csv(self):
        pass

    class Meta:
        db_table = 'DISTRICTS'


class SysDepartments(BaseModel):
    department_name = models.CharField(max_length=50, unique=True, db_column='DEPARTMENT_NAME')

    class Meta:
        db_table = 'SYS_DEPARTMENTS'
        indexes = [
            models.Index(fields=['department_name', 'objectid'])
        ]

    def __str__(self):
        return self.department_name


class Sectors(BaseModel):
    name = models.CharField(max_length=50, unique=True, db_column='SECTOR_NAME')

    class Meta:
        db_table = 'SECTORS'

    def __str__(self):
        return self.name


class SysPersonnel(BaseModel):
    firstname = models.CharField(max_length=50, db_column='FIRSTNAME')
    surname = models.CharField(max_length=50, db_column='SURNAME')
    username = models.CharField(max_length=50, db_column='USERNAME')
    department = models.ForeignKey(SysDepartments, on_delete=models.CASCADE)  # if department goes?
    position = models.CharField(max_length=50, db_column='POSITION')

    class Meta:
        db_table = 'SYS_PERSONNEL'

    def __str__(self):
        return self.username


class CheckAccount(BaseModel):
    objects = CheckAccountManager
    firm_type = models.CharField(max_length=50,
                                 choices=[('t', 'TUZEL_KISILIK'), ('s', 'SAHIS_ISLETMESI')],
                                 verbose_name='FIRM TYPE', help_text='Business type of the firm',
                                 db_column='FIRM_TYPE', null=True, default='t')
    firm_full_name = models.CharField(max_length=70, verbose_name='FIRM FULLNAME',
                                      db_column='FIRM_FULLNAME', null=True)
    taxpayer_number = models.CharField(unique=True, help_text='Sahis firmasi ise TCKNO, Tuzel Kisilik ise'
                                                              'Vergi No',
                                       db_column='TAXPAYER_NUMBER', max_length=15, null=True)

    # validators cannot be used
    birthplace = models.ForeignKey(Cities, on_delete=models.SET_NULL, related_name='birthplace', null=True, blank=True,
                                   verbose_name='Doğum Yeri')
    tax_department = models.CharField(max_length=100, verbose_name='TAX DEPARTMENT', db_column='TAX_DEPARTMENT',
                                      null=True)
    firm_address = models.CharField(max_length=200, verbose_name='FIRM ADDRESS', db_column='FIRM_ADDRESS', null=True)

    firm_key_contact_personnel = models.CharField(max_length=70,
                                                  verbose_name='Firm Contact Name',
                                                  db_column='FIRM_KEY_PERSON', null=True)
    sector = models.ForeignKey(Sectors, on_delete=models.SET_NULL, null=True, verbose_name='Sektör')

    city = models.ForeignKey(Cities, on_delete=models.SET_NULL, null=True,
                             verbose_name='Şehir')
    district = models.ForeignKey(Districts, on_delete=models.SET_NULL, null=True, verbose_name='İlçe')

    phone_number = models.CharField(max_length=15, unique=True, db_column='PHONE_NUMBER',
                                    verbose_name='Telefon numarası', null=True)
    fax = models.CharField(max_length=15, unique=True, db_column='FAX_NUMBER', verbose_name='Fax Numarası', null=True)
    web_url = models.URLField(db_column='WEB_URL', verbose_name='Web adresi', null=True)
    email_addr = models.EmailField(unique=True, db_column='EMAIL_ADDR', verbose_name='Email adresi', null=True)
    representative_person = models.ForeignKey(SysPersonnel, on_delete=models.SET_NULL,
                                              verbose_name='Temsilci', null=True)

    account_document = models.OneToOneField('AccountDocuments', on_delete=models.SET_NULL)

    class Meta:
        db_table = 'CHECKACCOUNT'
        indexes = [
            models.Index(fields=['city', 'district', 'customer']),
            models.Index(fields=['firm_type', 'firm_full_name', 'customer']),
            models.Index(fields=['customer', 'representative_person', 'firm_key_contact_personnel', 'birthplace'])
        ]

    def __str__(self):
        return self.firm_full_name

    def save(self, *args, **kwargs):
        # validators kullanılmayan kurallar
        if self.firm_type is None:
            LegalEntityMustHaveBirthPlace()

        if self.taxpayer_number is None:
            SoleTraderMustHaveTaxPayerNumber()

        super(CheckAccount, self).save(*args, **kwargs)


class AccountDocumentManager(models.Manager):
    pass


class BaseAccountDocument(BaseModel):
    customer = models.OneToOneField(CheckAccount, on_delete=models.SET_NULL)


class AccountDocuments(BaseAccountDocument):
    objects = AccountDocumentManager

    activity_certificate_pdf = models.FilePathField(
        upload_to='activity_certificates/pdfs/',
        verbose_name='Activity Certificate',
        db_column='ACTIVITY_CERTIFICATE_PATH', null=True, blank=True)

    tax_return_pdf = models.FilePathField(
        upload_to='tax_return/pdfs/', verbose_name='Tax Return',
        db_column='TAX_RETURN_PATH', null=True, blank=True)

    authorized_signatures_list_pdf = models.FilePathField(
        upload_to='authorized_signatures_list/pdfs/',
        verbose_name='Authorized Signatures List',
        db_column='AUTHORIZED_SIG_LIST', null=True, blank=True)

    class Meta:
        db_table = 'ACCOUNT_DOCUMENTS'

    def __str__(self):
        return f"Attachments of {self.customer}"


class PartnershipDocuments(BaseAccountDocument):
    partnership_structure_identity_copies = models.FilePathField('ORTAKLIK YAPISI VE KIMLIK KOPYALARI',
                                                                 allow_folders=True,
                                                                 db_column='PARTNERSHIP_STRUCTURE_PATH')

    identity_copies = models.FilePathField('KIMLIK KOPYALARI', allow_folders=True, db_column='IDENTITY_COPIES_PATH')
    board_management = models.FilePathField('YONETIM KURULU YAPISI', allow_folders=True,
                                            db_column='BOARD_MANAGEMENT_PATH')

    class Meta:
        db_table = 'PARTNERSHIP_DOCUMENTS'

    def __str__(self):
        return f"Partnership Documents of {self.customer_id}"


class CustomerBank(BaseAccountDocument):
    bank_name = models.CharField(max_length=60, unique=False, db_column='BANK_NAME')

    # diger bilgiler gelir.
    class Meta:
        db_table = "CUSTOMER_BANK"

    def __str__(self):
        return self.bank_name


class BaseBlackLists(BaseModel):
    firm_name = models.CharField(max_length=150)

    def find_related_customers(self, customer):
        pass

    class Meta:
        db_table = 'BLACK_LIST'


class RelatedBlackList(BaseBlackLists):
    class Meta:
        db_table = 'BLACK_LIST'

    def __str__(self):
        return f"Black list"

    def find_related_customers(self, customer):
        pass


class SystemBlackList(BaseBlackLists):
    class Meta:
        db_table = 'SYS_BLACK_LIST'

    def __str__(self):
        return f"System Black Lists"

    def find_related_customers(self, customer):
        pass


class KonkordatoList(BaseBlackLists):
    class Meta:
        db_table = 'KONKORDATO_LIST'

    def __str__(self):
        return f"Konkordato "

    def find_related_customers(self, customer):
        pass
