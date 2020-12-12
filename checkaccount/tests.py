import os
import warnings
from abc import ABC

# import shapefile
from django.test import TestCase
import geopandas as gpd
import pandas as pd

from .models import SysDepartments, SysPersonnel, Cities, Districts, CheckAccount, Sectors


class ImportCityDistricts(ABC):
    folder_path = r"C:\Users\LENOVO\PycharmProjects\DumanCPMS\testdata"

    def __init__(self, iller='iller.xlsx', ilceler='ilceler.xlsx'):
        self.iller_excel = os.path.join(self.folder_path, iller)
        self.ilce_excel = os.path.join(self.folder_path, ilceler)

    def read_from_excel(self):
        df_iller = pd.read_excel(self.iller_excel)
        df_ilceler = pd.read_excel(self.ilce_excel)

        return df_iller, df_ilceler

    def _save_iller(self, df):
        for index, row in df.iterrows():
            Cities.objects.get_or_create(name=row['adm1_en'])

    def _save_ilceler(self, df):
        for index, row in df.iterrows():
            Districts.objects.get_or_create(name=row['adm2_en'], city=Cities.objects.get(name=row['adm1_en']))

    def _save_excels(self):
        if len(Cities.objects.all()) > 5 and len(Districts.objects.all()) > 5:
            return

        df_iller, df_ilceler = self.read_from_excel()
        self._save_iller(df_iller)
        self._save_ilceler(df_ilceler)

    def runforme(self):
        self._save_excels()
        print("Imported city and districts")


class SysDepartmentsTest(TestCase):
    @staticmethod
    def test_create_test_departments():
        SysDepartments.objects.get_or_create(department_name='FINANCE')
        SysDepartments.objects.get_or_create(department_name='HR')
        SysDepartments.objects.get_or_create(department_name='IT')
        SysDepartments.objects.get_or_create(department_name='GIS')
        SysDepartments.objects.get_or_create(department_name='MIS')

    @staticmethod
    def test_get_all_departments():
        print("all departments : \n")
        print(SysDepartments.objects.all())


class SysPersonnelTest(TestCase):
    @staticmethod
    def test_create_personels():
        SysDepartmentsTest.test_create_test_departments()

        SysPersonnel.objects.get_or_create(firstname='mert', surname='öner', username='moner',
                                           department=SysDepartments.objects.get(department_name='FINANCE'),
                                           position='MARKETING')
        SysPersonnel.objects.get_or_create(firstname='umut', surname='ucok', username='uucok',
                                           department=SysDepartments.objects.get(department_name='MIS'),
                                           position='ENGINEER')
        SysPersonnel.objects.get_or_create(firstname='mustafa', surname='duman', username='mduman',
                                           department=SysDepartments.objects.get(department_name='IT'),
                                           position='CEO')
        SysPersonnel.objects.get_or_create(firstname='salim', surname='onurbilen', username='sonurbilen',
                                           department=SysDepartments.objects.get(department_name='GIS'),
                                           position='ENGINEER')
        SysPersonnel.objects.get_or_create(firstname='enes', surname='duman', username='eduman',
                                           department=SysDepartments.objects.get(department_name='IT'),
                                           position='CTO')
        print("many users were created !")


class SectorTest(TestCase):
    @staticmethod
    def test_create_sectors():
        Sectors.objects.get_or_create(name='FINANCE')
        Sectors.objects.get_or_create(name='GIS')
        Sectors.objects.get_or_create(name='IT')
        Sectors.objects.get_or_create(name='IOT')
        Sectors.objects.get_or_create(name='GAME DEVELOPMENT')
        Sectors.objects.get_or_create(name='AKILLI EV')

        print("Many sectors are created")


class CheckAccountTest(TestCase, ImportCityDistricts):
    excel_path = r"C:\Users\LENOVO\PycharmProjects\DumanCPMS\excels\CheckAccountsTest.xls"

    @staticmethod
    def test_create_one_account():
        # required tables and data
        SysPersonnelTest.test_create_personels()
        SectorTest.test_create_sectors()

        # district also imports cities
        ImportCityDistricts().runforme()

        s = Sectors.objects.get_or_create(name='GIS')
        s = s[0]
        sp = SysPersonnel.objects.get_or_create(username='sonurbilen')
        sp = sp[0]

        c = Cities.objects.get(name='CORUM')
        d = Districts.objects.get(name='ISKILIP', city=c)

        c = CheckAccount.objects.get_or_create(firm_type='SAHIS_ISLETMESI', firm_full_name='UMUT TEST AS',
                                               taxpayer_number=18319776776,
                                               tax_department='UMRANIYE VERGI DAIRESI',
                                               firm_address='sample address',
                                               firm_key_contact_personnel='someone',
                                               city=c,
                                               district=d,
                                               sector=s,
                                               phone_number='05063791026',
                                               fax='02122451517', web_url='https://dumanarge.com',
                                               email_addr='info@dumanarge.com',
                                               representative_person=sp)

        c = c[0]
        return c

    def test_create_accounts_from_excel(self):
        # required tables and data
        SysPersonnelTest.test_create_personels()
        SectorTest.test_create_sectors()
        ImportCityDistricts().runforme()

        df = self.read_from_excel()
        print("excel verisi : \n"
              "{}".format(df))

        for index, i in df.iterrows():
            firm_type = i['firm_type']
            firm_full_name = i['firm_full_name']
            taxpayer_number = i['taxpayer_number']
            birthplace = i['birthplace']
            tax_department = i['tax_department']
            firm_address = i['firm_address']
            firm_key_contact_personnel = i['firm_key_contact_personnel']
            sector = i['sector']
            city = i['city']
            district = i['district']
            phone_number = i['phone_number']
            fax = i['fax']
            web_url = i['web_url']
            email_addr = i['email_addr']
            representative_person = i['representative_person']

            # general information
            sector = Sectors.objects.get_or_create(name=sector)
            city = Cities.objects.get_or_create(city_name=city)
            district = Districts.objects.get_or_create(district_name=district)

            representative_person = SysPersonnel.objects.get_or_create(username=representative_person)

            CheckAccount.objects.get_or_create(firm_type=firm_type, firm_full_name=firm_full_name,
                                               taxpayer_number=taxpayer_number,
                                               birthplace=birthplace, tax_department=tax_department,
                                               firm_address=firm_address,
                                               firm_key_contact_personnel=firm_key_contact_personnel,
                                               sector=sector, city=city, district=district, phone_number=phone_number,
                                               fax=fax, web_url=web_url, email_addr=email_addr,
                                               representative_person=representative_person)

# attachment tests
