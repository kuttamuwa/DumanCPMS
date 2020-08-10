from django.db import models

from .geo_models import GeoModel
from .model_sys_specs import CariHesapSpecs, AccountDocumentsSpec, PartnershipDocumentsSpecs, \
    LegalEntityMustHaveBirthPlace, SoleTraderMustHaveTaxPayerNumber

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
    district_name = models.CharField(max_length=50, db_column='DISTRICT_NAME')
    related_city_name = models.ForeignKey(Cities, on_delete=models.CASCADE)

    def import_from_shapefile(self):
        pass

    def import_from_csv(self):
        pass

    class Meta:
        db_table = 'DISTRICTS'
        indexes = [
            models.Index(fields=['objectid', 'district_name'])
        ]


class SysDepartments(models.Model):
    department_name = models.CharField(max_length=50, unique=True, db_column='DEPARTMENT_NAME')
    objectid = models.AutoField(primary_key=True)

    class Meta:
        db_table = 'SYS_DEPARTMENTS'
        indexes = [
            models.Index(fields=['department_name', 'objectid'])
        ]


class Sectors(models.Model):
    name = models.CharField(max_length=50, unique=True, db_column='SECTOR_NAME')
    objectid = models.AutoField(primary_key=True)

    class Meta:
        db_table = 'SECTORS'


class SysPersonnel(models.Model):
    firstname = models.CharField(max_length=50, db_column='FIRSTNAME')
    surname = models.CharField(max_length=50, db_column='SURNAME')
    username = models.CharField(max_length=50, db_column='USERNAME')
    department = models.ForeignKey(SysDepartments, on_delete=models.CASCADE)  # if department goes?
    position = models.CharField(max_length=50, db_column='POSITION')

    personnel_id = models.AutoField(primary_key=True)

    class Meta:
        db_table = 'SYS_PERSONNEL'
        indexes = [
            models.Index(fields=['firstname', 'personnel_id', 'department']),
            models.Index(fields=['personnel_id', 'firstname', 'surname'])
        ]


class CheckAccount(models.Model):
    firm_type = models.CharField(max_length=50, choices=CariHesapSpecs.get_firm_type_choices(),
                                 verbose_name='FIRM TYPE', help_text='Business type of the firm',
                                 db_column='FIRM_TYPE')
    firm_full_name = models.CharField(max_length=70, verbose_name='FIRM FULLNAME',
                                      db_column='FIRM_FULLNAME')
    taxpayer_number = models.CharField(unique=True, help_text='Sahis firmasi ise TCKNO, Tuzel Kisilik ise'
                                                              'Vergi No',
                                       db_column='TAXPAYER_NUMBER', max_length=15)

    # validators cannot be used
    birthplace = models.ForeignKey(Cities, on_delete=models.CASCADE, related_name='birthplace', null=True, blank=True)
    tax_department = models.CharField(max_length=100, verbose_name='TAX DEPARTMENT', db_column='TAX_DEPARTMENT')
    firm_address = models.CharField(max_length=200, verbose_name='FIRM ADDRESS', db_column='FIRM_ADDRESS')

    firm_key_contact_personnel = models.CharField(max_length=70,
                                                  verbose_name=CariHesapSpecs.get_key_contact_personnel(),
                                                  db_column='FIRM_KEY_PERSON')
    sector = models.ForeignKey(Sectors, on_delete=models.SET_NULL, null=True)

    city = models.ForeignKey(Cities, on_delete=models.SET_NULL, null=True)  # if city | district goes?
    district = models.ForeignKey(Districts, on_delete=models.SET_NULL, null=True)

    phone_number = models.CharField(max_length=15, unique=True, db_column='PHONE_NUMBER')
    fax = models.CharField(max_length=15, unique=True, db_column='FAX_NUMBER')
    web_url = models.URLField(db_column='WEB_URL')
    email_addr = models.EmailField(unique=True, db_column='EMAIL_ADDR')
    representative_person = models.ForeignKey(SysPersonnel, on_delete=models.PROTECT)  # there is still job to do?

    # object id
    customer_id = models.AutoField(primary_key=True)

    class Meta:
        db_table = CariHesapSpecs.get_table_name()
        indexes = [
            models.Index(fields=['city', 'district', 'customer_id']),
            models.Index(fields=['firm_type', 'firm_full_name', 'customer_id']),
            models.Index(fields=['customer_id', 'representative_person', 'firm_key_contact_personnel', 'birthplace'])
        ]

    def save(self, *args, **kwargs):
        # validators kullanılmayan kurallar

        if CariHesapSpecs.check_legal_entity(self.firm_type):
            # sahis firmasi
            if self.birthplace is None:
                raise LegalEntityMustHaveBirthPlace()

        else:
            # tuzel kisilik
            if self.taxpayer_number is None:
                raise SoleTraderMustHaveTaxPayerNumber()

        super(CheckAccount, self).save(*args, **kwargs)


class AccountDocuments(models.Model):
    activity_certificate = models.FilePathField(
        verbose_name=AccountDocumentsSpec.get_activity_certificate_verbose_name(),
        db_column='ACTIVITY_CERTIFICATE_PATH')
    tax_return = models.FilePathField(verbose_name=AccountDocumentsSpec.get_tax_return_verbose_name(),
                                      db_column='TAX_RETURN_PATH')
    authorized_signatures_list = models.FilePathField(
        verbose_name=AccountDocumentsSpec.get_authorized_signatures_list_verbose_name(),
        db_column='AUTHORIZED_SIG_LIST')

    attachment_id = models.AutoField(primary_key=True)

    # if customer was deleted?
    customer_id = models.ForeignKey(CheckAccount, on_delete=models.CASCADE)

    class Meta:
        db_table = 'ACCOUNT_DOCUMENTS'
        indexes = [
            models.Index(fields=['attachment_id', 'customer_id'])
        ]


class PartnershipDocuments(models.Model):
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

    class Meta:
        db_table = 'PARTNERSHIP_DOCUMENTS'
        indexes = [
            models.Index(fields=['attachment_id', 'customer_id'])
        ]

    def save(self, *args, **kwargs):
        super(PartnershipDocuments, self).save(*args, **kwargs)

# class RelatedBlackList(models.Model):
#     objectid = models.AutoField(primary_key=True)
#     customer_id = models.ForeignKey(CheckAccount, on_delete=models.PROTECT)
#
#     # todo: and many fields
#
#     class Meta:
#         db_table = 'BLACK_LIST'
