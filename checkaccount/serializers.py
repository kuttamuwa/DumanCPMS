from rest_framework import serializers
from .models import Tutorial, CheckAccount


class TutorialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutorial
        fields = ('id',
                  'title',
                  'description',
                  'published')


class CheckAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckAccount
        fields = ('firm_type',
                  'firm_full_name',
                  'people_id',
                  'birthplace',
                  'tax_number',
                  'tax_department',
                  'firm_address',
                  'firm_key_contact_personnel',
                  'sector',
                  'city',
                  'district',
                  'phone_number',
                  'fax', 'web_url', 'email_addr', 'customer_id'
                  'representative_person'
                  )


# class BlackListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = BlackList
#         fields = ()  # todo: fill later.
