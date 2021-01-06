from rest_framework import routers
from dashboard.views import CheckAccountAPI

router = routers.DefaultRouter()

router.register(r'checkaccount', CheckAccountAPI)
