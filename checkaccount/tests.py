import os
import warnings
from abc import ABC

# import shapefile
from django.test import TestCase
import geopandas as gpd
import pandas as pd

from .models import SysDepartments, SysPersonnel, Cities, Districts, CheckAccount, Sectors
from .models import CariHesapSpecs


class ImportFromShapefile(TestCase, ABC):
    shpfile_folder = r"C:\Users\umut\PycharmProjects\DumanCPMS\geodata\turkeyshp"
    target_shpfile = ""

    city_name_field = "adm1_en"  # related city name also
    district_name_field = "adm2_en"
    plate_number_field = "adm1"  # same with district

    def import_from_shapefile(self):
        print("import from shapefile test has begun")

        file = os.path.join(self.shpfile_folder, self.target_shpfile)
        if os.path.exists(file):
            df = gpd.read_file(file)
            return df

        else:
            warnings.warn(f"{file} shapefile could not be found !")


class ImportFromExcelfile(ABC):
    excel_path = None

    def read_from_excel(self, *args, **kwargs):
        if self.excel_path is None:
            raise ValueError("Excel path could not be found !")

        df = pd.read_excel(self.excel_path, *args, **kwargs)
        return df


class CitiesTest(ImportFromShapefile):
    target_shpfile = 'iller/iller.shp'

    def test_import_cities(self):
        print("import from shapefile test has begun - CITIES ")
        df = self.import_from_shapefile()
        for i in df.iterrows():
            c_name = i[1][self.city_name_field]
            p_number = i[1][self.plate_number_field][4:]
            print(f"city : {c_name}  -  plate : {p_number}")
            Cities.objects.create(city_name=c_name, city_plate_number=p_number)


class DistrictTest(ImportFromShapefile):
    target_shpfile = 'ilceler/ilceler.shp'

    def test_import_all_districts_shp(self):
        CitiesTest().test_import_cities()

        print("import from shapefile test has begun - DISTRICT")
        df = self.import_from_shapefile()

        for i in df.iterrows():
            related_c_name = i[1][self.city_name_field]
            d_name = i[1][self.district_name_field]
            print(f"related city name : {related_c_name}   -   district name : {d_name}")
            Districts.objects.create(related_city_name=Cities.objects.get(city_name=related_c_name),
                                     district_name=d_name)

        print("all districts are imported")


class SysDepartmentsTest(TestCase):
    @staticmethod
    def test_create_test_departments():
        SysDepartments.objects.create(department_name='FINANCE')
        SysDepartments.objects.create(department_name='HR')
        SysDepartments.objects.create(department_name='IT')
        SysDepartments.objects.create(department_name='GIS')
        SysDepartments.objects.create(department_name='MIS')

    @staticmethod
    def test_get_all_departments():
        print("all departments : \n")
        print(SysDepartments.objects.all())


class SysPersonnelTest(TestCase):
    @staticmethod
    def test_create_personels():
        SysDepartmentsTest.test_create_test_departments()

        SysPersonnel.objects.create(firstname='mert', surname='öner', username='moner',
                                    department=SysDepartments.objects.get(department_name='FINANCE'),
                                    position='MARKETING')
        SysPersonnel.objects.create(firstname='umut', surname='ucok', username='uucok',
                                    department=SysDepartments.objects.get(department_name='MIS'),
                                    position='ENGINEER')
        SysPersonnel.objects.create(firstname='mustafa', surname='duman', username='mduman',
                                    department=SysDepartments.objects.get(department_name='IT'),
                                    position='CEO')
        SysPersonnel.objects.create(firstname='salim', surname='onurbilen', username='sonurbilen',
                                    department=SysDepartments.objects.get(department_name='GIS'),
                                    position='ENGINEER')
        SysPersonnel.objects.create(firstname='enes', surname='duman', username='eduman',
                                    department=SysDepartments.objects.get(department_name='IT'),
                                    position='CTO')
        print("many users were created !")


class SectorTest(TestCase):
    @staticmethod
    def test_create_sectors():
        Sectors.objects.get_or_create(name='GIS')
        Sectors.objects.get_or_create(name='IT')
        Sectors.objects.get_or_create(name='IOT')
        Sectors.objects.get_or_create(name='GAME DEVELOPMENT')
        Sectors.objects.get_or_create(name='AKILLI EV')


class CheckAccountTest(TestCase, ImportFromExcelfile):
    excel_path = r"C:\Users\umut\PycharmProjects\DumanCPMS\excels\CheckAccountsTest.xls"

    @staticmethod
    def test_create_one_account():
        # required tables and data
        SysPersonnelTest.test_create_personels()
        SectorTest.test_create_sectors()

        # district also imports cities
        DistrictTest().test_import_all_districts_shp()

        CheckAccount.objects.create(firm_type='SAHIS_ISLETMESI', firm_full_name='UMUT TEST AS',
                                    taxpayer_number=18319776776,
                                    birthplace=Cities.objects.get(city_name='CORUM'),
                                    tax_department='UMRANIYE VERGI DAIRESI',
                                    firm_address='sample address',
                                    firm_key_contact_personnel='someone',
                                    sector=Sectors.objects.get(name='GIS'), city=Cities.objects.get(city_name='CORUM'),
                                    district=Districts.objects.get(district_name='ISKILIP'), phone_number='05063791026',
                                    fax='02122451517', web_url='https://dumanarge.com', email_addr='info@dumanarge.com',
                                    representative_person=SysPersonnel.objects.get(username='sonurbilen'))

    def test_create_accounts_from_excel(self):
        # required tables and data
        SysPersonnelTest.test_create_personels()
        SectorTest.test_create_sectors()

        # district also imports cities
        DistrictTest().test_import_all_districts_shp()

        df = self.read_from_excel()
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

            # foreign keys relations
            if CariHesapSpecs.check_legal_entity(firm_type):
                birthplace = Cities.objects.get(city_name=birthplace)
            else:
                birthplace = None

            # general information
            sector = Sectors.objects.get(name=sector)
            city = Cities.objects.get(city_name=city)
            district = Districts.objects.get(district_name=district)

            representative_person = SysPersonnel.objects.get(username=representative_person)

            CheckAccount.objects.create(firm_type=firm_type, firm_full_name=firm_full_name,
                                        taxpayer_number=taxpayer_number,
                                        birthplace=birthplace, tax_department=tax_department,
                                        firm_address=firm_address,
                                        firm_key_contact_personnel=firm_key_contact_personnel,
                                        sector=sector, city=city, district=district, phone_number=phone_number,
                                        fax=fax, web_url=web_url, email_addr=email_addr,
                                        representative_person=representative_person)


# attachment tests

