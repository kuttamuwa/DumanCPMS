from haystack import indexes

from checkaccount.models import CheckAccount


class CheckAccountIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    firm_type = indexes.CharField(model_attr='firm_type')
    firm_full_name = indexes.CharField(model_attr='firm_full_name')
    taxpayer_number = indexes.CharField(model_attr='taxpayer_number')

    def get_model(self):
        return CheckAccount

    def index_queryset(self, using=None):
        return self.get_model().objects.filter()
