from django.contrib.auth.models import User
from django.db import models

from .basemodels import GeoModel, BaseModel
from .errors import SoleTraderMustHaveTaxPayerNumber, LegalEntityMustHaveBirthPlace
from .fields import DumanModelFileField


class Cities(GeoModel):
    city_plate_number = models.PositiveSmallIntegerField(db_column='CITY_PLATE_NUMBER', unique=True,
                                                         null=True)

    def import_from_shapefile(self):
        pass

    def import_from_csv(self):
        pass

    class Meta:
        db_table = 'CITIES'


class Districts(GeoModel):
    city = models.ForeignKey(Cities, on_delete=models.CASCADE, null=True)

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

    def __str__(self):
        return self.department_name


class Sectors(BaseModel):
    name = models.CharField(max_length=50, unique=False, db_column='SECTOR_NAME', null=True)

    class Meta:
        db_table = 'SECTORS'

    def __str__(self):
        return self.name


class SysPersonnel(BaseModel):
    firstname = models.CharField(max_length=50, db_column='FIRSTNAME', null=True, unique=False)
    surname = models.CharField(max_length=50, db_column='SURNAME', null=True, unique=False)
    username = models.CharField(max_length=50, db_column='USERNAME', null=True, unique=False) # True
    department = models.ForeignKey(SysDepartments, on_delete=models.CASCADE, null=True,
                                   unique=False)  # if department goes?
    position = models.CharField(max_length=50, db_column='POSITION', null=True)

    class Meta:
        db_table = 'SYS_PERSONNEL'

    def __str__(self):
        return self.username


class CheckAccountManager(models.Manager):
    def create(self, *args, **kwargs):
        return super(CheckAccountManager, self).create(*args, **kwargs)


class CheckAccount(BaseModel):
    firm_type = models.CharField(max_length=50, choices=[('t', 'TUZEL_KISILIK'), ('s', 'SAHIS_ISLETMESI')],
                                 verbose_name='FIRM TYPE', help_text='Business type of the firm',
                                 db_column='FIRM_TYPE', null=True, default='t')
    firm_full_name = models.CharField(max_length=70, verbose_name='FIRM FULLNAME',
                                      db_column='FIRM_FULLNAME', null=True)
    taxpayer_number = models.CharField(unique=False,
                                       help_text='Sahis firmasi ise TCKNO, Tuzel Kisilik ise Vergi No',
                                       db_column='TAXPAYER_NUMBER', max_length=15, null=True)

    # validators cannot be used
    birthplace = models.ForeignKey(Cities, on_delete=models.CASCADE, related_name='birthplace',
                                   null=True, blank=True, verbose_name='Doğum Yeri')
    tax_department = models.CharField(max_length=100, verbose_name='TAX DEPARTMENT', db_column='TAX_DEPARTMENT',
                                      null=True)
    firm_address = models.CharField(max_length=200, verbose_name='FIRM ADDRESS', db_column='FIRM_ADDRESS', null=True)

    firm_key_contact_personnel = models.ForeignKey(SysPersonnel, max_length=70, on_delete=models.SET_NULL,
                                                   verbose_name='Firm Contact Name', null=True)
    sector = models.ForeignKey(Sectors, on_delete=models.SET_NULL, null=True, verbose_name='Sektör')

    city = models.ForeignKey(Cities, on_delete=models.SET_NULL, null=True,
                             verbose_name='Şehir')  # if city | district goes?
    district = models.ForeignKey(Districts, on_delete=models.SET_NULL, null=True, verbose_name='İlçe')

    phone_number = models.CharField(max_length=15, unique=False, db_column='PHONE_NUMBER',
                                    verbose_name='Telefon numarası', null=True)
    fax = models.CharField(max_length=15, unique=False, db_column='FAX_NUMBER', verbose_name='Fax Numarası', null=True)
    web_url = models.URLField(db_column='WEB_URL', verbose_name='Web adresi', null=True)
    email_addr = models.EmailField(unique=False, db_column='EMAIL_ADDR', verbose_name='Email adresi', null=True)

    class Meta:
        db_table = 'CHECKACCOUNT'

    def __str__(self):
        return self.firm_full_name

    def save(self, *args, **kwargs):
        # validators kullanılmayan kurallar

        if self.firm_type is None:
            LegalEntityMustHaveBirthPlace()

        if self.taxpayer_number is None:
            SoleTraderMustHaveTaxPayerNumber()

        super(CheckAccount, self).save(*args, **kwargs)


class BaseAccountDocument(BaseModel):
    customer = models.ForeignKey(CheckAccount, on_delete=models.SET_NULL, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"Attachments of {self.customer}"


class AccountDocuments(BaseAccountDocument):
    activity_certificate_pdf = DumanModelFileField(
        upload_to='activity_certificates/pdfs/',
        verbose_name='Activity Certificate',
        db_column='ACTIVITY_CERTIFICATE_PATH', null=True, blank=True)

    tax_return_pdf = DumanModelFileField(
        upload_to='tax_return/pdfs/', verbose_name='Tax Return',
        db_column='TAX_RETURN_PATH', null=True, blank=True)

    authorized_signatures_list_pdf = DumanModelFileField(
        upload_to='authorized_signatures_list/pdfs/',
        verbose_name='Authorized Signatures List',
        db_column='AUTHORIZED_SIG_LIST', null=True, blank=True)

    class Meta:
        db_table = 'ACCOUNT_DOCUMENTS'

    def delete_by_type(self, _type):
        if _type == 1:
            self.activity_certificate_pdf.delete()

        elif _type == 2:
            self.tax_return_pdf.delete()

        elif _type == 3:
            self.authorized_signatures_list_pdf.delete()


class PartnershipDocuments(BaseAccountDocument):
    # klasörde depolanabilir
    partnership_structure_identity_copies = models.FilePathField('ORTAKLIK YAPISI VE KIMLIK KOPYALARI',
                                                                 allow_folders=True,
                                                                 db_column='PARTNERSHIP_STRUCTURE_PATH')

    identity_copies = models.FilePathField('KIMLIK KOPYALARI',
                                           allow_folders=True,
                                           db_column='IDENTITY_COPIES_PATH')
    board_management = models.FilePathField('YONETIM KURULU YAPISI',
                                            allow_folders=True, db_column='BOARD_MANAGEMENT_PATH')

    class Meta:
        db_table = 'PARTNERSHIP_DOCUMENTS'


class BaseBlackLists(BaseModel):
    firm_name = models.CharField(max_length=150)

    def find_related_customers(self, customer):
        pass

    class Meta:
        db_table = 'BLACK_LIST'
        abstract = True

    def __str__(self):
        return 'Abstract Black List Object'


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
