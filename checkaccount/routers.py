from rest_framework import routers

from checkaccount.api import CheckAccountAPI, AccountDocumentsAPI, PartnershipDocumentsAPI, SectorsAPI, SysPersonnelAPI
from checkaccount.api import CitiesAPI, DistrictAPI

router = routers.DefaultRouter()

router.register(r'accounts', CheckAccountAPI)
router.register(r'adocs', AccountDocumentsAPI)
router.register(r'pdocs', PartnershipDocumentsAPI)
router.register(r'sectors', SectorsAPI)
router.register(r'syspersonnels', SysPersonnelAPI)
router.register(r'cities', CitiesAPI)
router.register(r'district', DistrictAPI)