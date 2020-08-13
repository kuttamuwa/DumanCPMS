from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Column, Row, Fieldset, ButtonHolder
from crispy_forms.tests.forms import forms

from checkaccount.model_sys_specs import CariHesapSpecs
from checkaccount.models import CheckAccount


# class CheckAccountForm(forms.ModelForm):
    # class Meta:
    #     model = CheckAccount

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #
    #     self.helper.layout = Layout(
    #         Fieldset(
    #             'firm_type',
    #             'firm_full_name',
    #             # 'favorite_number',
    #             # 'favorite_color',
    #             # 'favorite_food',
    #             # 'notes'
    #         ),
    #         ButtonHolder(
    #             Submit('submit', 'Submit', css_class='button white')
    #         )
    #     )
    #     # self.helper.layout = Layout(
    #     #
    #     #     Column('firm_type', css_class='form-group col-md-6 mb-0'),
    #     #     Column('firm_full_name', css_class='form-group col-md-6 mb-0'),
    #     #     # css_class='form-row'
    #     # ,
    #     # Row(
    #     #     Column('taxpayer_number', css_class='form-group col-md-6 mb-0'),
    #     #     Column('birthplace', css_class='form-group col-md-6 mb-0'),
    #     #     Column('tax_department', css_class='form-group col-md-6 mb-0'),
    #     #     Column('firm_address', css_class='form-group col-md-4 mb-0'),
    #     #     Column('sector', css_class='form-group col-md-2 mb-0'),
    #     #     Column('city', css_class='form-group col-md-2 mb-0'),
    #     #     Column('district', css_class='form-group col-md-2 mb-0'),
    #     #
    #     #     Column('phone_number', css_class='form-group col-md-2 mb-0'),
    #     #     Column('fax', css_class='form-group col-md-2 mb-0'),
    #     #     Column('web_url', css_class='form-group col-md-2 mb-0'),
    #     #     Column('email_addr', css_class='form-group col-md-2 mb-0'),
    #     #     Column('representative_person', css_class='form-group col-md-2 mb-0'),
    #     #     css_class='form-row'
    #     # ),
    #     # Submit('submit', 'Sign in'),
    #     # )
