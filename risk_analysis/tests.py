from django.test import TestCase

import pandas as pd


# Create your tests here.
from risk_analysis.models import DataSetModel


# class DataSetImportExcel(TestCase):
#     excel_file = r"C:\Users\umut\PycharmProjects\DumanCPMS\risk_analysis\data"
#
#     def test_import_from_excel(self):
#         df = pd.read_excel(self.excel_file)
#         for index, i in df.iterrows():
#             DataSetModel.objects.get_or_create(i)
