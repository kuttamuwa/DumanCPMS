from rest_framework import routers

from checkaccount.api import CheckAccountAPI, AccountDocumentsAPI, PartnershipDocumentsAPI, SectorsAPI, SysPersonnelAPI

router = routers.DefaultRouter()

router.register(r'accounts', CheckAccountAPI)
router.register(r'adocs', AccountDocumentsAPI)
router.register(r'pdocs', PartnershipDocumentsAPI)
router.register(r'sectors', SectorsAPI)
router.register(r'syspersonnels', SysPersonnelAPI)
