from rest_framework import routers

from dashboard.api import CheckAccountAPI, RiskAnalysisAPI

router = routers.DefaultRouter()

router.register(r'checkaccount', CheckAccountAPI)
router.register(r'riskanalysis', RiskAnalysisAPI)

