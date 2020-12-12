from django.contrib.auth.models import User
from django.db import models

from .errors import SoleTraderMustHaveTaxPayerNumber, LegalEntityMustHaveBirthPlace
from .fields import DumanModelFileField
from .geo_models import GeoModel
from .model_sys_specs import CariHesapSpecs, AccountDocumentsSpec, PartnershipDocumentsSpecs

"""
UYARILAR:
Firmaya özel Kara liste, geçmiş kara listesi aktarılır
Vergi borcu olanlar listeden uyarı
SGK borcu olanlar listeden uyarı
Sistemdeki tüm kullanıcıların verisine dayalı kara liste uygulaması
Konkordato listesi alınabilri mi

Müşteri çekilirken kayıt sayısı sistemdeki ile uyuşmazsa hata verir

"""


class Cities(GeoModel):
    city_name = models.CharField(max_length=50, db_column='CITY_NAME', unique=True)
    city_plate_number = models.PositiveSmallIntegerField(db_column='CITY_PLATE_NUMBER', unique=True, db_index=True)
    created = models.DateTimeField(auto_now_add=True)

    def import_from_shapefile(self):
        pass

    def import_from_csv(self):
        pass

    class Meta:
        db_table = 'CITIES'
        indexes = [
            models.Index(fields=['city_name'])
        ]

    def __str__(self):
        return self.city_name


class Districts(GeoModel):
    district_name = models.CharField(max_length=50, db_column='DISTRICT_NAME')
    related_city_name = models.ForeignKey(Cities, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def import_from_shapefile(self):
        pass

    def import_from_csv(self):
        pass

    class Meta:
        db_table = 'DISTRICTS'
        indexes = [
            models.Index(fields=['objectid', 'district_name'])
        ]

    # todo : ilce isimleri ile gore filtrelenerek getirilmeli. Kontrol icin admin sayfasına bak.
    def __str__(self):
        return self.district_name


class SysDepartments(models.Model):
    department_name = models.CharField(max_length=50, unique=True, db_column='DEPARTMENT_NAME')
    objectid = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'SYS_DEPARTMENTS'
        indexes = [
            models.Index(fields=['department_name', 'objectid'])
        ]

    def __str__(self):
        return self.department_name


class Sectors(models.Model):
    name = models.CharField(max_length=50, unique=True, db_column='SECTOR_NAME')
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'SECTORS'

    def __str__(self):
        return self.name


class SysPersonnel(models.Model):
    firstname = models.CharField(max_length=50, db_column='FIRSTNAME')
    surname = models.CharField(max_length=50, db_column='SURNAME')
    username = models.CharField(max_length=50, db_column='USERNAME')
    department = models.ForeignKey(SysDepartments, on_delete=models.CASCADE)  # if department goes?
    position = models.CharField(max_length=50, db_column='POSITION')

    personnel_id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'SYS_PERSONNEL'
        indexes = [
            models.Index(fields=['firstname', 'personnel_id', 'department']),
            models.Index(fields=['personnel_id', 'firstname', 'surname'])
        ]

    def __str__(self):
        return self.username


class CheckAccountManager(models.Manager):
    def create(self, *args, **kwargs):
        return super(CheckAccountManager, self).create(*args, **kwargs)


class CheckAccount(models.Model):
    firm_type = models.CharField(max_length=50, choices=CariHesapSpecs.get_firm_type_choices(),
                                 verbose_name='FIRM TYPE', help_text='Business type of the firm',
                                 db_column='FIRM_TYPE', null=True, default='t')
    firm_full_name = models.CharField(max_length=70, verbose_name='FIRM FULLNAME',
                                      db_column='FIRM_FULLNAME', null=True)
    taxpayer_number = models.CharField(unique=True, help_text='Sahis firmasi ise TCKNO, Tuzel Kisilik ise'
                                                              'Vergi No',
                                       db_column='TAXPAYER_NUMBER', max_length=15, null=True)

    # validators cannot be used
    birthplace = models.ForeignKey(Cities, on_delete=models.CASCADE, related_name='birthplace', null=True, blank=True,
                                   verbose_name='Doğum Yeri')
    tax_department = models.CharField(max_length=100, verbose_name='TAX DEPARTMENT', db_column='TAX_DEPARTMENT',
                                      null=True)
    firm_address = models.CharField(max_length=200, verbose_name='FIRM ADDRESS', db_column='FIRM_ADDRESS', null=True)

    firm_key_contact_personnel = models.CharField(max_length=70,
                                                  verbose_name=CariHesapSpecs.get_key_contact_personnel(),
                                                  db_column='FIRM_KEY_PERSON', null=True)
    sector = models.ForeignKey(Sectors, on_delete=models.SET_NULL, null=True, verbose_name='Sektör')

    city = models.ForeignKey(Cities, on_delete=models.SET_NULL, null=True,
                             verbose_name='Şehir')  # if city | district goes?
    district = models.ForeignKey(Districts, on_delete=models.SET_NULL, null=True, verbose_name='İlçe')

    phone_number = models.CharField(max_length=15, unique=True, db_column='PHONE_NUMBER',
                                    verbose_name='Telefon numarası', null=True)
    fax = models.CharField(max_length=15, unique=True, db_column='FAX_NUMBER', verbose_name='Fax Numarası', null=True)
    web_url = models.URLField(db_column='WEB_URL', verbose_name='Web adresi', null=True)
    email_addr = models.EmailField(unique=True, db_column='EMAIL_ADDR', verbose_name='Email adresi', null=True)
    representative_person = models.ForeignKey(SysPersonnel, on_delete=models.PROTECT,
                                              verbose_name='Temsilci', null=True)

    # object id
    customer_id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = CariHesapSpecs.get_table_name()
        indexes = [
            models.Index(fields=['city', 'district', 'customer_id']),
            models.Index(fields=['firm_type', 'firm_full_name', 'customer_id']),
            models.Index(fields=['customer_id', 'representative_person', 'firm_key_contact_personnel', 'birthplace'])
        ]

    @classmethod
    def get_auto_fields(cls):
        return 'customer_id',

    def __str__(self):
        return self.firm_full_name

    def save(self, *args, **kwargs):
        # validators kullanılmayan kurallar

        if CariHesapSpecs.check_legal_entity(self.firm_type):
            # sahis firmasi
            if self.birthplace is None:
                LegalEntityMustHaveBirthPlace()

        else:
            # tuzel kisilik
            if self.taxpayer_number is None:
                SoleTraderMustHaveTaxPayerNumber()

        super(CheckAccount, self).save(*args, **kwargs)


class AccountDocuments(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    activity_certificate_pdf = DumanModelFileField(
        upload_to='activity_certificates/pdfs/',
        verbose_name=AccountDocumentsSpec.get_activity_certificate_verbose_name(),
        db_column='ACTIVITY_CERTIFICATE_PATH', null=True, blank=True)

    tax_return_pdf = DumanModelFileField(
        upload_to='tax_return/pdfs/', verbose_name=AccountDocumentsSpec.get_tax_return_verbose_name(),
        db_column='TAX_RETURN_PATH', null=True, blank=True)

    authorized_signatures_list_pdf = DumanModelFileField(
        upload_to='authorized_signatures_list/pdfs/',
        verbose_name=AccountDocumentsSpec.get_authorized_signatures_list_verbose_name(),
        db_column='AUTHORIZED_SIG_LIST', null=True, blank=True)

    attachment_id = models.AutoField(primary_key=True)

    # if customer was deleted?
    customer_id = models.OneToOneField(CheckAccount, on_delete=models.PROTECT)
    attachment_title = models.CharField(unique=False, null=True, blank=True, max_length=50, db_column='TITLE')
    description = models.CharField(unique=False, null=True, blank=True, max_length=250, db_column='DESCRIPTION')

    class Meta:
        db_table = 'ACCOUNT_DOCUMENTS'
        indexes = [
            models.Index(fields=['attachment_id', 'customer_id'])
        ]

    def __str__(self):
        return f"{self.description}//{self.customer_id}"

    def delete_by_type(self, _type):
        if _type == 1:
            # activity_certificate_pdf
            self.delete_activity_certificate()

        elif _type == 2:
            # tax_return_pdf
            self.delete_tax_return_pdf()

        elif _type == 3:
            # authorized_signatures_list_pdf
            self.delete_authorized_signatures_list_pdf()

    def delete_activity_certificate(self):
        self.activity_certificate_pdf.delete()

    def delete_tax_return_pdf(self):
        self.tax_return_pdf.delete()

    def delete_authorized_signatures_list_pdf(self):
        self.authorized_signatures_list_pdf.delete()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        return super(AccountDocuments, self).save(force_insert, force_update, using, update_fields)


class PartnershipDocuments(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    # klasörde depolanabilir
    partnership_structure_identity_copies = models.FilePathField(
        PartnershipDocumentsSpecs.get_partnership_structure_id_copies_verbose_name(), allow_folders=True,
        db_column='PARTNERSHIP_STRUCTURE_PATH')

    identity_copies = models.FilePathField(PartnershipDocumentsSpecs.get_identity_copies_verbose_name(),
                                           allow_folders=True,
                                           db_column='IDENTITY_COPIES_PATH')
    board_management = models.FilePathField(PartnershipDocumentsSpecs.get_board_structure_verbose_name(),
                                            allow_folders=True, db_column='BOARD_MANAGEMENT_PATH')

    # if customer was deleted?
    customer_id = models.ForeignKey(CheckAccount, on_delete=models.CASCADE, db_column='CUSTOMER_ID')
    attachment_id = models.AutoField(primary_key=True)
    attachment_title = models.CharField(unique=False, null=True, blank=True, max_length=50, db_column='TITLE')
    description = models.CharField(unique=False, null=True, blank=True, max_length=250, db_column='DESCRIPTION')

    class Meta:
        db_table = 'PARTNERSHIP_DOCUMENTS'
        indexes = [
            models.Index(fields=['attachment_id', 'customer_id'])
        ]

    def save(self, *args, **kwargs):
        super(PartnershipDocuments, self).save(*args, **kwargs)

    def __str__(self):
        return f"attach//{self.customer_id}//{self.attachment_id}"


class CustomerBank(models.Model):
    # musteri silinirse kayit da silinir
    customer_id = models.ForeignKey(CheckAccount, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True, db_column='ID')
    bank_name = models.CharField(max_length=60, unique=False, db_column='BANK_NAME')

    # diger bilgiler gelir.
    class Meta:
        db_table = "CUSTOMER_BANK"

    def __str__(self):
        return self.bank_name


class RelatedBlackList(models.Model):
    id = models.AutoField(primary_key=True, db_column='ID')
    customer_id = models.ForeignKey(CheckAccount, on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)

    # todo: and many fields

    class Meta:
        db_table = 'BLACK_LIST'

    def __str__(self):
        return f"Black list for {CheckAccount.objects.get(customer_id=self.customer_id)}"

    def get_customer_name(self):
        return CheckAccount.objects.get(customer_id=self.customer_id).firm_full_name


class SystemBlackList(RelatedBlackList):
    class Meta:
        db_table = 'SYS_BLACK_LIST'

    def __str__(self):
        return f"System Black List for {self.get_customer_name()}"


class KonkordatoList(RelatedBlackList):
    class Meta:
        db_table = 'KONKORDATO_LIST'

    def __str__(self):
        return f"Konkordato for {self.get_customer_name()}"
