from django.db import models

try:
    from checkaccount.models import CheckAccount as usermodel
    from checkaccount.models import DummyCreator as dcreator

except ImportError:
    from risk_analysis.basemodels import DummyUser as usermodel
    from risk_analysis.basemodels import DummyCreator as dcreator


class UserAdaptorManager(models.Manager):
    def create(self, *args, **kwargs):
        super(UserAdaptorManager, self).create(*args, **kwargs)


class UserAdaptor(usermodel):
    objects = UserAdaptorManager()
    dummy_creator = dcreator()

    def __str__(self):
        return self.firm_full_name