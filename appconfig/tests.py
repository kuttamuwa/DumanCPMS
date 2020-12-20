import os

from django.test import TestCase

# Create your tests here.
from appconfig.models import Domains, Subtypes
import pandas as pd


class ImportAllDomains(TestCase):
    excel_path = os.path.join(os.path.abspath('.'), 'appconfig', 'data', 'Domains.xlsx')

    @staticmethod
    def create_all_domains():
        Domains.objects.create()

    @classmethod
    def import_all_domains(cls):
        df = pd.read_excel(cls.excel_path)
        for index, row in df.iterrows():
            Domains.objects.get_or_create(**row)

    @classmethod
    def export_all_domains(cls):
        df = pd.DataFrame(Domains.objects.all().values())
        df.drop(columns=['data_id', 'created_date', 'created_by_id',
                         'basemodel_ptr_id'], inplace=True)
        df.to_excel(cls.excel_path)


class ImportAllSubtypes(TestCase):
    excel_path = os.path.join(os.path.abspath('.'), 'appconfig', 'data', 'Subtypes.xlsx')

    @staticmethod
    def create_all_subtypes():
        Subtypes.objects.create()

    @classmethod
    def import_subtypes(cls):
        df = pd.read_excel(cls.excel_path)
        for index, row in df.iterrows():
            Subtypes.objects.get_or_create(**row)

    @classmethod
    def export_excel(cls):
        df = pd.DataFrame(Subtypes.objects.all().values())
        df.drop(columns=['data_id', 'created_date', 'created_by_id',
                         'basemodel_ptr_id'], inplace=True)

        df.to_excel(cls.excel_path, sheet_name='Subtypes')
