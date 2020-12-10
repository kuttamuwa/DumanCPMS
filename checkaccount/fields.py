from django.db import models


class DumanFileField(models.FileField):
    def _require_file(self):
        pass  # default

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
