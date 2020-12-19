from django.db import models
from django.conf import settings


class BaseModel(models.Model):
    # objects = models.Manager

    data_id = models.AutoField(primary_key=True)

    created_date = models.DateTimeField(auto_now_add=True, db_column='CREATED_DATE',
                                        verbose_name='Created Date')

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,
                                   on_delete=models.SET_NULL, verbose_name='Created by')

    # edited_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'RISK_BASEMODEL'


class DummyCreator(models.Manager):
    def generate_dummy_username(self):
        max_value = self.model.objects.all().last().pk
        default_value = self.model.username.field.default
        username = default_value + f"_{max_value}"

        return username

    def create_dummy(self, username=None):
        if username is None:
            username = self.generate_dummy_username()

        return self.create(username=username)


class DummyUser(BaseModel):
    username = models.CharField(max_length=50, default='dummy', unique=True, null=False, blank=True)
    dummy_creator = DummyCreator()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(DummyUser, self).save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.username
